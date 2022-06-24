from hashlib import new
import os, sys, time, json
from telnetlib import IP
from re import T

class DB:
    def __init__(self, dbName:str="db.json", reloadTimer:int=5, syncTimer:int=2) -> None:
        # Initialize the object
        self.dbName:str = dbName
        self.reloadTimer:int = reloadTimer
        self.syncTimer:int = syncTimer
        self.startTime:float = time.time()
        self.reloadTime:float = 0
        self.lastSync:float = 0
        self.loaded:bool = False
        self.data:dict = {}
        self.lock:bool = False
        self.discovery = None
        self.mac = None
        
        # Reload the database
        self._reload()
        
    def _reload(self) -> bool:
        try:
            with open("data/"+self.dbName, 'r') as f:
                _RAW = f.read()
                try:
                    self.data = json.loads(_RAW)
                    self.loaded = True
                    return True
                except:
                    print("Database corrupted")
                    os._exit(0)
        except OSError:
            print("Database read error")
            os._exit(100)
            
    def reload(self) -> bool:
        _DELTA:float = time.time() - self.reloadTime
        if _DELTA >= self.reloadTimer:
            # Wait until unlocked
            while self.lock: continue
            # Reload the DB
            self.reloadTime = time.time()
            self.lock = True
            self._reload()
            self.lock = False
            return True
        else: return False
        
    def _update(self):
        try:
            with open("data/"+self.dbName, 'w') as f:
                try:
                    f.write(json.dumps(self.data, indent=2))
                    return True
                except:
                    print("Database error while writing data")
                    return False
        except OSError:
            print("Database write error")
            return False
            
    def update(self):
        # Wait until unlocked
        while self.lock: continue
        # Lock the database
        self.lock = True
        # Update the DB file
        self._update()
        # Unlock the database
        self.lock = False
        
    def sync(self, force=False):
        _DELTA:float = time.time() - self.lastSync
        if _DELTA > self.syncTimer or force:
            self.update()
            self.lastSync = time.time()
            return True
        return False
        
    def getDevices(self):
        if not self.loaded: return None
        self.reload()
        return self.data["devices"]
    
    def updateDevices(self, devices:dict):
        self.data["devices"] = devices
        self.sync()
        return True
    
    def getDeviceByMac(self, mac:str) -> dict:
        return
    
    def setDiscovery(self, discovery) -> None:
       self.discovery = discovery 
       
    def setMac(self, mac:object) -> None:
        self.mac = mac
        
    def getMacIPList(self) -> list:
        output = []
        
        return output
    
    def autoInsert(self, scanResult:list):
        # Foreach device in the scan result list
        for dev in scanResult:
            # Get additional information about the device
            hostname:str = self.discovery.getHostName(dev["ip"])
            macInfo = self.mac.search(dev["mac"])
            macVendor = macInfo["vendorName"] if macInfo is not None else "unknown"
            # Mac Metadata
            if dev["mac"] not in self.data["history"]["mac_metadata"]:
                # Initialize the dict
                self.data["history"]["mac_metadata"][dev["mac"]] = {
                    "first_seen": int(time.time()), # First seen timestamp
                    "notes": "",                # Notes about the device
                    "trusted": False,           # Device flagged as trusted
                    "type": "generic",          # Device type (eg. router, switch, etc.)
                    "os": "unknown",            # Device OS (eg. Windows, Linux, Mac, etc.)
                    "os_version": "unknown",    # Device OS version (eg "10" for Windows 10)
                    "location": "unknown",      # Device location (eg "Bedroom")
                    "name": "Unknown Device",   # Device custom name (eg "Tom laptop")
                    "connected_via": "unknown", # Wire/Wifi/Bluetooth/USB/power plug/...
                    "connected_thru": "unknown",# Other device MAC address
                    "mac_vendor": macVendor,    # Mac cached vendor name
                    "ip_list": [dev["ip"], ]    # List of IP addresses used by the device
                }
            # Update metadata
            self.data["history"]["mac_metadata"][dev["mac"]]["last_seen"] = int(time.time())
            self.data["history"]["mac_metadata"][dev["mac"]]["hostname"] = hostname
            # Update the IP used by this mac
            if not dev["ip"] in self.data["history"]["mac_metadata"][dev["mac"]]["ip_list"]:
                self.data["history"]["mac_metadata"][dev["mac"]]["ip_list"].append(dev["ip"])
            