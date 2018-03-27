import re


def cleanse_mac_wifi_scan_res(response):
    connections = response.split('\n')
    headers = _combine_info(connections[0], headers=True)
    return [
        dict(zip(headers, _combine_info(connection_info)))
        for connection_info in connections[1:]
        if connection_info
    ]


def _combine_info(wifi_info, headers=False):
    wifi_info = wifi_info.split()
    security_info = wifi_info[6:]
    wifi_info = wifi_info[:6]
    wifi_info.append(' '.join(security_info))
    if not headers:
        bssid_idx = next(
            idx for idx, el in enumerate(wifi_info)
            if re.match(r'([0-9A-Fa-f]{2}([:-]|$)){6}', el)
        )
        ssid = ' '.join(wifi_info[:bssid_idx])
        wifi_info = wifi_info[(bssid_idx-1):]
        wifi_info[0] = ssid

    return wifi_info
