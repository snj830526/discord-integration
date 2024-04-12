import os
import requests
import json

code_file = 'market_codes.json'

class OtherApp():
    
    def __init__(self):
        print('new start')
        pass
    
    
    def getMarketCodes(self):
        saved = self.readCodes()
        if saved == None or len(saved) == 0:
            url = f"https://api.upbit.com/v1/market/all?isDetails=true"
            headers = {"accept": "application/json"}
            res = requests.get(url, headers=headers)
            return self.saveCodes(res.json())
        else:
            return saved
        
        
    def refreshMarketCodes(self):
        
        if os.path.isfile(code_file):
            os.remove(code_file)
            
        return self.getMarketCodes()
    
    
    def saveCodes(self, codes):
        
        print('writing codes')
        with open(code_file, 'w') as json_file:
            json.dump(codes, json_file)
        
        return codes
        


    def readCodes(self):
        
        if os.path.isfile(code_file):    
            with open(code_file, 'r') as json_file:
                if json_file != None:
                    codes = json.load(json_file)
                    return codes
                else:
                    return dict()
        else:
            return dict()