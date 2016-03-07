[![Build Status](https://travis-ci.org/joshvillbrandt/wireless.svg?branch=master)](https://travis-ci.org/joshvillbrandt/wireless) [![Documentation Status](https://readthedocs.org/projects/wireless/badge/?version=latest)](http://wireless.readthedocs.org/en/latest/)

# wireless

A dead simple, cross-platform Python library to connect to wireless networks.

## Description

This library can control a computer's wireless adapter to connect to a network. Environments currently supported include (in order of preference):

Network Manager | Operating Systems | Tested Adapters
--- | --- | ---
nmcli | Ubuntu 12.04, 14.04 | Linksys AE3000, Intel Centrino 6250
wpa_supplicant | Ubuntu 12.04, 14.04 | Intel Centrino 6250
networksetup | Mac OS 10.10 | Macbook Pro



## Setup

```bash
sudo pip install wireless
```

## Usage

A typical usage looks like this:

```python
from wireless import Wireless
wireless = Wireless()
wireless.connect(ssid='ssid', password='password')
```

Note: To use `nmcli` on Ubuntu 14.04, the right permissions must be in place. A few options are listed [here](https://wiki.archlinux.org/index.php/NetworkManager#Set_up_PolicyKit_permissions).

Note: To use `wpa_supplicant`, `network-manager` (the backend for `nmcli`) must not be running. This is because `network-manager` runs an instance of `wpa_supplicant` behind the scenes which will conflict with the `wpa_supplicant` instance that this library would create. If you have a `network-manager` on your machine but would prefer to use `wpa_supplicant` (not recommended), run `sudo service network-manager stop` before using `wireless`.

## API

* `Wireless([interface])` - initialize the wireless driver
* `connect(ssid, password)` - attempts to connect to a network and returns True on success
* `current()` - returns the name of the current network or None otherwise
* `interfaces()` - list the available interfaces
* `interface([interface])` - get or set the current interface
* `power([True||False])` - get or set the power status of the adapter
* `driver()` - return the name of driver being used for wireless control

## Change History

This project uses [semantic versioning](http://semver.org/).

### v0.3.2 - 2016/03/06

* Added a few tests and fixed a py34 bug ([XayOn](https://github.com/XayOn))

### v0.3.1 - 2015/04/24

* Added version check for nmcli ([Silarn](https://github.com/Silarn))

### v0.3.0 - 2015/01/13

* Added support for `wpa_supplicant`
* Added the `driver()` method

### v0.2.1 - 2014/12/01

* remove dependency on `pandoc`

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

## Publishing

First, install `pandoc` so that setup.py can auto-convert Markdown syntax into reStructuredText:

```bash
sudo apt-get install pandoc
sudo pip install pypandoc
```

Then, following [this guide](http://peterdowns.com/posts/first-time-with-pypi.html), push the project to PyPI:

```bash
sudo python setup.py sdist upload -r pypi
```
