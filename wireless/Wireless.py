from abc import ABCMeta, abstractmethod
import subprocess


# send a command to the shell and return the result
def cmd(cmd):
    return subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()


# abstracts away wireless connection
class Wireless:
    _driver = None

    # init
    def __init__(self, interface=None):
        # detect and init appropriate driver
        name = self._detectDriver()
        if name == 'nmcli':
            self._driver = NmcliWireless(interface=interface)
        elif name == 'networksetup':
            self._driver = NetworksetupWireless(interface=interface)

        # attempt to auto detect the interface if none was provided
        if self.interface() is None:
            interfaces = self.interfaces()
            if len(interfaces) > 0:
                self.interface(interfaces[0])

        # raise an error if there is still no interface defined
        if self.interface() is None:
            raise Exception('Unabled to auto-detect the network interface.')

    def _detectDriver(self):
        # try nmcli (Ubuntu 14.04)
        response = cmd('which nmcli')
        if len(response) > 0 and 'not found' not in response:
            return 'nmcli'

        # try networksetup (Mac OS 10.10)
        response = cmd('which networksetup')
        if len(response) > 0 and 'not found' not in response:
            return 'networksetup'

        raise Exception('Cannot find compatible wireless API.')

    # connect to a network
    def connect(self, ssid, password):
        return self._driver.connect(ssid, password)

    # return the ssid of the current network
    def current(self):
        return self._driver.current()

    # return a list of wireless adapters
    def interfaces(self):
        return self._driver.interfaces()

    # return the current wireless adapter
    def interface(self, interface=None):
        return self._driver.interface(interface)

    # return the current wireless adapter
    def power(self, power=None):
        return self._driver.power(power)


# abstract class for all wireless drivers
class WirelessDriver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self, ssid, password):
        pass

    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def interfaces(self):
        pass

    @abstractmethod
    def interface(self, interface=None):
        pass

    @abstractmethod
    def power(self, power=None):
        pass


# Linux nmcli Driver
class NmcliWireless(WirelessDriver):
    _interface = None

    # init
    def __init__(self, interface=None):
        self.interface(interface)

    # clean up connections where partial is part of the connection name
    # this is needed to prevent the following error after extended use:
    # 'maximum number of pending replies per connection has been reached'
    def _clean(self, partial):
        # list matching connections
        response = cmd('nmcli --fields UUID,NAME con list | grep {}'.format(
            partial))

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                uuid = line.split()[0]
                cmd('nmcli con delete uuid {}'.format(uuid))

    # ignore warnings in nmcli output
    # sometimes there are warnings but we connected just fine
    def _errorInResponse(self, response):
        # no error if no response
        if len(response) == 0:
            return False

        # loop through each line
        for line in response.splitlines():
            # all error lines start with 'Error'
            if line.startswith('Error'):
                return True

        # if we didn't find an error then we are in the clear
        return False

    # connect to a network
    def connect(self, ssid, password):
        # clean up previous connection
        self._clean(self.current())

        # attempt to connect
        response = cmd('nmcli dev wifi connect {} password {} iface {}'.format(
            ssid, password, self._interface))

        # parse response
        return not self._errorInResponse(response)

    # returned the ssid of the current network
    def current(self):
        # list active connections for all interfaces
        response = cmd('nmcli con status | grep {}'.format(
            self.interface()))

        # the current network is in the first column
        for line in response.splitlines():
            if len(line) > 0:
                return line.split()[0]

        # return none if there was not an active connection
        return None

    # return a list of wireless adapters
    def interfaces(self):
        # grab list of interfaces
        response = cmd('nmcli dev')

        # parse response
        interfaces = []
        for line in response.splitlines():
            if 'wireless' in line:
                # this line has our interface name in the first column
                interfaces.append(line.split()[0])

        # return list
        return interfaces

    # return the current wireless adapter
    def interface(self, interface=None):
        if interface is not None:
            self._interface = interface
        else:
            return self._interface

    # enable/disable wireless networking
    def power(self, power=None):
        if power is True:
            cmd('nmcli nm wifi on')
        elif power is False:
            cmd('nmcli nm wifi off')
        else:
            response = cmd('nmcli nm wifi')
            return 'enabled' in response


# OS X networksetup Driver
class NetworksetupWireless(WirelessDriver):
    _interface = None

    # init
    def __init__(self, interface=None):
        self.interface(interface)

    # connect to a network
    def connect(self, ssid, password):
        # attempt to connect
        response = cmd('networksetup -setairportnetwork {} {} {}'.format(
            self._interface, ssid, password))

        # parse response - assume success when there is no response
        return (len(response) == 0)

    # returned the ssid of the current network
    def current(self):
        # attempt to get current network
        response = cmd('networksetup -getairportnetwork {}'.format(
            self._interface))

        # parse response
        phrase = 'Current Wi-Fi Network: '
        if phrase in response:
            return response.replace('Current Wi-Fi Network: ', '').strip()
        else:
            return None

    # return a list of wireless adapters
    def interfaces(self):
        # grab list of interfaces
        response = cmd('networksetup -listallhardwareports')

        # parse response
        interfaces = []
        detectedWifi = False
        for line in response.splitlines():
            if detectedWifi:
                # this line has our interface name in it
                interfaces.append(line.replace('Device: ', ''))
                detectedWifi = False
            else:
                # search for the line that has 'Wi-Fi' in it
                if 'Wi-Fi' in line:
                    detectedWifi = True

        # return list
        return interfaces

    # return the current wireless adapter
    def interface(self, interface=None):
        if interface is not None:
            self._interface = interface
        else:
            return self._interface

    # enable/disable wireless networking
    def power(self, power=None):
        if power is True:
            cmd('networksetup -setairportpower {} on'.format(
                self._interface))
        elif power is False:
            cmd('networksetup -setairportpower {} off'.format(
                self._interface))
        else:
            response = cmd('networksetup -getairportpower {}'.format(
                self._interface))
            return 'On' in response
