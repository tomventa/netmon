from hashlib import new
import os, sys, time, json
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
                    f.write(json.dumps(self.data))
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
    
    def autoInsert(self, scanResult:list):
        for dev in scanResult:
            # Mac To Ip
            """
            newMacRecord = [dev["ip"], int(time.time())]
            if dev["mac"] not in self.data["history"]["mac_to_ip"]:
                self.data["history"]["mac_to_ip"][dev["mac"]] = []
                self.data["history"]["mac_to_ip"][dev["mac"]].append(newMacRecord)
            else:
                lastIP = self.data["history"]["mac_to_ip"][dev["mac"]][-1][0]
                if lastIP!=dev["ip"]:
                    self.data["history"]["mac_to_ip"][dev["mac"]].append(newMacRecord)
            # IP to Mac Address
            newIPRecord = [dev["mac"], int(time.time())]
            if dev["ip"] not in self.data["history"]["ip_to_mac"]:
                self.data["history"]["ip_to_mac"][dev["ip"]] = []
                self.data["history"]["ip_to_mac"][dev["ip"]].append(newIPRecord)
            else:
                lastMac = self.data["history"]["ip_to_mac"][dev["ip"]][-1][0]
                if lastMac!=dev["mac"]:
                    self.data["history"]["ip_to_mac"][dev["ip"]].append(newIPRecord)
            """
            