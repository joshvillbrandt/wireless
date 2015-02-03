import os

import Wireless

# Example Vista output for "netsh wlan show profiles"

"""

Profiles on interface Wireless Network Connection:

Group Policy Profiles (read only)
---------------------------------
    <None>

User Profiles
-------------
    All User Profile     : cashvault
    All User Profile     : IBM-guest
    All User Profile     : Guakamole

"""
def get_win_profiles():
    output = Wireless.cmd("netsh wlan show profiles")
    names = []
    for line in output.splitlines():
        if "All User Profile" in line:
            names.append(line.split(":")[-1].strip())
    return names

# Example Vista output for "netsh wlan show profile <name>"

"""
...
Connectivity settings
---------------------
    Number of SSIDs        : 1
    SSID name              : "cashvault"
    Network type           : Infrastructure
    Radio type             : [ Any Radio Type ]
    Vendor extension       : Not present
...
"""
def get_win_profile_ssid(profile):
    output = Wireless.cmd("netsh wlan show profile \"%s\"" % profile)
    for line in output.splitlines():
        if "SSID name" in line:
            return line.split(":")[-1].strip(' "')


if os.name == 'nt':
    print("[*] Get WiFi profiles")
    profiles = get_win_profiles()
    print("[*] Scanning profiles for given SSID")
    for prof in profiles:
        print get_win_profile_ssid(prof)
