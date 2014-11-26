[![Build Status](https://travis-ci.org/joshvillbrandt/wireless.svg?branch=master)](https://travis-ci.org/joshvillbrandt/wireless) [![Documentation Status](https://readthedocs.org/projects/wireless/badge/?version=latest)](http://wireless.readthedocs.org/en/latest/)

# wireless

A dead simple, cross-platform Python library to connect to wireless networks.

## Description

This library can control a computer's wireless adapter to connect to a network. Environments currently supported include:

Operating System | Network Managers | Tested Adapters
--- | --- | ---
Ubuntu 12.04, 14.04 | nmcli | Linksys AE3000, Intel Centrino 6250
Mac OS 10.10 | networksetup | Macbook Pro

## Setup

```bash
sudo pip install wireless
```

To use the `nmcli` on Ubuntu 14.04, the right permissions must be in place. A few options are listed [here](https://wiki.archlinux.org/index.php/NetworkManager#Set_up_PolicyKit_permissions).

## Usage

A typical usage looks like this:

```python
from wireless import Wireless
wireless = Wireless()
wireless.connect(ssid='ssid', password='password')
```

## API

* `Wireless([interface])` - initialize the wireless driver
* `connect(ssid, password)` - attempts to connect to a network and returns True on success
* `current()` - returns the name of the current network or None otherwise
* `interfaces()` - list the available interfaces
* `interface(interface)` - get or set the current interface
* `power(power=True||False)` - get or set the power status of the adapter

## Change History

This project uses [semantic versioning](http://semver.org/).

### v0.2.0 - 2014/11/25

* Added support for multiple network adapters with `interface()` and `interfaces()` methods
* The `current()` method actually asks the wireless driver for the current SSID instead of returning the name of the most recently connected network
* Added the `power()` method

### v0.1.1 - 2014/11/24

* Better documentation formatting for PyPI

### v0.1.0 - 2014/11/22

* Initial release

## Contributions

Pull requests to the `develop` branch are welcomed!
