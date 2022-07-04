from __future__ import absolute_import, division, print_function
from tabnanny import verbose
from tkinter import N
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import errno
import getopt
import os, sys, io, time, json, math
from scapy.all import *
from scapy.layers.inet import IP, ICMP

class Discovery:
    def __init__(self) -> None:
        self.mac = None
        pass
    
    def setMac(self, mac) -> None:
        self.mac = mac
    
    def long2net(self, arg):
        if (arg <= 0 or arg >= 0xFFFFFFFF):
            raise ValueError("Illegal netmask value", hex(arg))
        return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))
    
    def toCIDRNotation(self, bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = self.long2net(bytes_netmask)
        net = "%s/%s" % (network, netmask)
        return None if netmask<16 else net
    
    def getHostName(self, ip:str) -> str:
        try:
            hostname = socket.gethostbyaddr(ip)
            return hostname[0]
        except socket.herror:
            return None
        
    def getOS(self, target:str) -> str:
        pack = IP(dst=target)/ICMP()
        resp = sr1(pack, timeout=3, verbose=0)
        if resp:
            if IP in resp:
                ttl = resp.getlayer(IP).ttl
                if ttl <= 64: 
                    return 'Linux'
                elif ttl > 64:
                    return 'Windows'
                else:
                    return 'Unknown'
        else: return "Unknown"
    
    def _scan(self, net:str, interface:str, timeout:int=2, resolveHostname:bool=False) -> list:
        try:
            ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=False)
            devices = []
            for s, r in ans.res:
                # Get IP and MAC address
                device = {"ip":"", "mac":"", "hostname":""}
                device["ip"] = r.psrc
                device["mac"] = r.src
                # Resolve the hostname
                if resolveHostname:
                    device["hostname"] = self.resolveHostname(r.psrc)
                # Add this device to the final list
                devices.append(device)
                print(device)
            return devices
        except socket.error as e:
            if e.errno == errno.EPERM:     # Operation not permitted
                print(f"{e.strerror}. Did you run as root?")
            else:
                raise
            
    def scan(self, interface_to_scan=None):
        for network, netmask, _, interface, address, _ in scapy.config.conf.route.routes:
            # Skip if the interface is selected and not this one
            if interface_to_scan and interface_to_scan != interface:
                continue
            
            # Skip loopback network and default gateway
            if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
                continue

            # Skip interfaces with netmask 255.255.255.255 or empty
            if netmask <= 0 or netmask == 0xFFFFFFFF:
                continue

            # Skip docker interface
            if interface != interface_to_scan \
                    and (interface.startswith('docker')
                        or interface.startswith('br-')
                        or interface.startswith('tun')):
                continue

            # Gte CIDR notation (ip/n)
            net = self.toCIDRNotation(network, netmask)

            # If network CIDR is not empty
            if net:
                print("Scanning", net, interface)
                return self._scan(net, interface)
                
    