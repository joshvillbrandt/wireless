[![Build Status](https://travis-ci.org/joshvillbrandt/wireless.svg?branch=master)](https://travis-ci.org/joshvillbrandt/wireless) [![Documentation Status](https://readthedocs.org/projects/wireless/badge/?version=latest)](https://readthedocs.org/projects/wireless/?badge=latest)

# wireless

A dead simple, cross-platform Python library to connect to wireless networks.

## Description

This library can control a computer's wireless adapter to connect to a network. Environments currently supported include:

* Mac OS 10.10
* Ubuntu 12.04

## Setup

```bash
sudo pip install wireless
```

To use the `nmcli` on Ubuntu, one must have the right permissions in place. A few options are listed [here](https://wiki.archlinux.org/index.php/NetworkManager#Set_up_PolicyKit_permissions).

## Usage

A typical usage looks like this:

```python
from wireless import Wireless
wireless = Wireless()
wireless.connect(ssid='ssid', password='password')
```

## API

* `Wireless()` - initialize the wifi driver
* `connect(ssid, password)` - attempts to connect to a network and returns True on success
* `current()` - returns the name of the current network or None otherwise

## Change History

This project uses [semantic versioning](http://semver.org/).

### v0.1.1 - 2014/11/24

* Better documentation formatting for PyPI

### v0.1.0 - 2014/11/22

* Initial release

## Contributions

Pull requests to the `develop` branch are welcomed!
