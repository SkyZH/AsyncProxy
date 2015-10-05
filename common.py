# From Shadowsocks common.py

import struct
import socket

ADDRTYPE_IPV4 = 1
ADDRTYPE_IPV6 = 4
ADDRTYPE_HOST = 3

def parse_header(data):
    addrtype = data[0]
    dest_addr = None
    dest_port = None
    header_length = 0
    if addrtype == ADDRTYPE_IPV4:
        if len(data) >= 7:
            dest_addr = socket.inet_ntoa(data[1:5])
            dest_port = struct.unpack('>H', data[5:7])[0]
            header_length = 7
        else:
            logging.warn('header is too short')
    elif addrtype == ADDRTYPE_HOST:
        if len(data) > 2:
            addrlen = data[1]
            if len(data) >= 2 + addrlen:
                dest_addr = data[2:2 + addrlen].decode()
                dest_port = struct.unpack('>H', data[2 + addrlen:4 +
                                                     addrlen])[0]
                header_length = 4 + addrlen
            else:
                logging.warn('header is too short')
        else:
            logging.warn('header is too short')
    elif addrtype == ADDRTYPE_IPV6:
        if len(data) >= 19:
            dest_addr = socket.inet_ntop(socket.AF_INET6, data[1:17])
            dest_port = struct.unpack('>H', data[17:19])[0]
            header_length = 19
        else:
            logging.warn('header is too short')
    else:
        logging.warn('unsupported addrtype %d, maybe wrong password or '
                     'encryption method' % addrtype)
    if dest_addr is None:
        return None
    return addrtype, dest_addr, dest_port, header_length
