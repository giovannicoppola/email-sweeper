#!/usr/bin/python3 

### python script to interact with Complice



import requests
import json
COMPLICE_TOKEN = 'djnnamrjux6asm4ixub8'
COMPLICE_INTENTION = '&) email'

def get_emailZID(intention):
    
    url= 'https://complice.co/api/v0/u/me/today/core.json?auth_token='+COMPLICE_TOKEN 
    resp = requests.get(url)
    
    myResponse =  (resp.json())
    intentions = myResponse['list']
    myZID = ''
    for xx in intentions:
        if xx["text"] == intention:
            myZID = xx["zid"]
            break
    
    return myZID
    

def post_intention(intention):
    
    url = 'https://complice.co/api/v0/u/me/intentions?auth_token='+COMPLICE_TOKEN 
    datastring = dict()
    
    datastring['raw'] = intention
    datastring['response'] = "today"
    
    resp = requests.post(url,data=datastring)
    
    myResponse =  (resp.json())
    intentions = myResponse['core']['list']
    myZID = ''
    for xx in intentions:
        if xx["text"] == intention:
            myZID = xx["zid"]
            break
    
    return myZID
    
    
    
def addPomo(zid,dur):
    url = 'https://complice.co/api/v0/u/me/add_dur?auth_token='+COMPLICE_TOKEN 
    datastring = {}
    datastring ['ty'] = 'sand'
    datastring ['min'] = dur
    datastring ['zidToAssignTo'] = zid
    resp = requests.post(url,data=datastring)


def main():
    
    myZID = ''
    myZID = get_emailZID(COMPLICE_INTENTION)
    
    
    if myZID:
        
        addPomo(myZID,10)
    else:
        myZID = post_intention(COMPLICE_INTENTION)
        addPomo(myZID,10)


    

if __name__ == "__main__":
    main()