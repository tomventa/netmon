from __future__ import absolute_import, division, print_function
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import errno
import getopt
import os, sys, io, time, json, math

class Discovery:
    def __init__(self) -> None:
        pass
    
    def long2net(self, arg):
        if (arg <= 0 or arg >= 0xFFFFFFFF):
            raise ValueError("Illegal netmask value", hex(arg))
        return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))
    
    def to_CIDR_notation(self, bytes_network, bytes_netmask):
        network = scapy.utils.ltoa(bytes_network)
        netmask = self.long2net(bytes_netmask)
        net = "%s/%s" % (network, netmask)
        return None if netmask<16 else net
    
    def _scan(self, net, interface, timeout=2):
        try:
            ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=False)
            devices = []
            for s, r in ans.res:
                # Get IP and MAC address
                device = {"ip":"", "mac":"", "hostname":""}
                device["ip"] = r.psrc
                device["mac"] = r.src
                # Resolve the hostname
                try:
                    #hostname = socket.gethostbyaddr(r.psrc)
                    #device["hostname"] = hostname[0]
                    device["hostname"] = "test"
                except socket.herror:
                    # failed to resolve
                    device["hostname"] = None
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
            net = self.to_CIDR_notation(network, netmask)

            # If network CIDR is not empty
            if net:
                print("Scanning", net, interface)
                return self._scan(net, interface)
                
    