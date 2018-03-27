def cleanse_mac_wifi_scan_res(response):
    connections = response.split('\n')
    headers = _combine_wifi_security_info(connections[0])
    return [
        dict(zip(headers, _combine_wifi_security_info(connection_info)))
        for connection_info in connections[1:]
    ]


def _combine_wifi_security_info(wifi_info):
    wifi_info = wifi_info.split()
    security_info = wifi_info[6:]
    wifi_info = wifi_info[:6]
    wifi_info.append(' '.join(security_info))
    return wifi_info
