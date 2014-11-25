from abc import ABCMeta, abstractmethod
import subprocess


# attempt to retrieve the iwlist response for a given ssid
def cmd(cmd):
    return subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()


# abstracts away the wifi details
class Wireless:
    _driver = None

    # init
    def __init__(self):
        name = self._detect()
        if name == 'nmcli':
            self._driver = NmcliWireless()
        elif name == 'networksetup':
            self._driver = NetworksetupWireless()

    def _detect(self):
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
    def connect(self, **kwargs):
        return self._driver.connect(**kwargs)

    # returned the ssid of the current network
    def current(self, **kwargs):
        return self._driver.current(**kwargs)


# abstract class for all wireless drivers
class WirelessDriver:
    __metaclass__ = ABCMeta

    # connect to a network
    @abstractmethod
    def connect(self, ssid, password):
        pass

    # returned the ssid of the current network
    @abstractmethod
    def current(self):
        pass


# Ubuntu Driver
class NmcliWireless(WirelessDriver):
    _currentSSID = None

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
        if self._currentSSID is not None:
            self._clean(self._currentSSID)

        # attempt to connect
        response = cmd('nmcli dev wifi connect {} password {}'.format(
            ssid, password))

        # parse response
        if self._errorInResponse(response):
            self._currentSSID = None
            return False
        else:
            self._currentSSID = ssid
            return True

    # returned the ssid of the current network
    def current(self):
        # TODO: actually check the current SSID with a shell call
        # nmcli dev wifi | grep yes
        return self._currentSSID


# OS X Driver
class NetworksetupWireless(WirelessDriver):
    _interface = None
    _currentSSID = None

    # init
    def __init__(self):
        self._interface = self._autoDetectInterface()

    def _autoDetectInterface(self):
        # grab list of interfaces
        response = cmd('networksetup -listallhardwareports')

        # parse response
        detectedWifi = False
        for line in response.splitlines():
            if detectedWifi:
                # this line has our interface name in it
                return line.replace('Device: ', '')
            else:
                # search for the line that has 'Wi-Fi' in it
                if 'Wi-Fi' in line:
                    detectedWifi = True

        # if we are here then we failed to auto detect the interface
        raise Exception('Unabled to auto-detect the network interface.')

    # connect to a network
    def connect(self, ssid, password):
        # attempt to connect
        response = cmd('networksetup -setairportnetwork {} {} {}'.format(
            self._interface, ssid, password))

        # parse response
        if len(response) == 0:
            self._currentSSID = ssid
            return True
        else:
            self._currentSSID = None
            return False

    # returned the ssid of the current network
    def current(self):
        # TODO: actually check the current SSID with a shell call
        return self._currentSSID
