import socket
from urllib.parse import urlparse
import ipaddress

PRIVATE_IP_RANGES = [
    '10.0.0.0/8',
    '172.16.0.0/12',
    '192.168.0.0/16',
    '127.0.0.0/8',
    '169.254.0.0/16',
    '::1/128',
    'fc00::/7',
]

def is_private_ip(ip):
    try:
        addr = ipaddress.ip_address(ip)
        for net in PRIVATE_IP_RANGES:
            if addr in ipaddress.ip_network(net):
                return True
        return False
    except:
        return True

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urlparse(url)
    if not parsed.netloc:
        return False
    try:
        host = parsed.netloc.split(':')[0]
        ip = socket.gethostbyname(host)
        if is_private_ip(ip):
            return False
        return True
    except:
        return False