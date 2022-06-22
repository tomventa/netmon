import os, io, sys, time, json


class Mac:
    def __init__(self):
        self.loaded:bool = False
        self.data:list = []
        self.load()
        
    def load(self):
        try:
            with open("data/mac.json", "r", encoding='utf8') as f:
                self.data = json.load(f)
                self.loaded = True
        except OSError:
            return
        
    def search(self, mac:str="ff:ff:ff:ff:ff:ff"):
        query = str(mac[0:8]).upper()
        print(query)
        for line in self.data:
            if query==line["macPrefix"]:
                return line
        return None