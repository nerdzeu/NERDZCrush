import json
from mediacrush.config import _cfg
from flask import request, current_app, redirect
from flaskext.bcrypt import generate_password_hash
from netaddr import all_matching_cidrs

def get_ip():
    ip = request.remote_addr
    if (all_matching_cidrs(ip, [_cfg("trusted_proxies")]) != []) and "X-Forwarded-For" in request.headers:
        ip = request.headers.get("X-Forwarded-For")
    return ip

def makeMask(n):
    "return a mask of n bits as a long integer"
    return (2 << n - 1) - 1


def dottedQuadToNum(ip):
    "convert decimal dotted quad string to long integer"
    parts = ip.split(".")
    return int(parts[0]) | (int(parts[1]) << 8) | (int(parts[2]) << 16) | (int(parts[3]) << 24)


def networkMask(ip, bits):
    "Convert a network address to a long integer"
    return dottedQuadToNum(ip) & makeMask(bits)


def addressInNetwork(ip, net):
    "Is an address in a network"
    return ip & net == net

def secure_ip():
    ip = get_ip()
    if is_tor():
        ip = 'anonymous_user'
    return generate_password_hash(ip)

def is_tor():
    return _cfg("tor_domain") and get_ip() == '127.0.0.1'
