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
        """Search for the macadress prefix in the json

        Args:
            mac (str): Input MacAddress. Example: "ff:ff:ff:ff:ff:ff".

        Returns:
            dict: Dictionary with the result.
        """
        # Wait until loaded
        while not self.loaded: continue
        # Search for the most complete macadress prefix
        for i in range(3, len(mac)-4):
            # Get the macadress prefix
            query = str(mac[0:(len(mac)-i)]).upper()
            # Skip useless invalid prefixes
            if query[-1]==":": continue
            # Compare the two prefixes
            for line in self.data:
                if query==line["macPrefix"]:
                    return line
        # If not found, return None
        return None