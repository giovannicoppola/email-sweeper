#!/usr/bin/python3 

## email Sprinter
# 
##  – Light snow, mist 🌨  🌡️+31°F (feels +22°F, 85%) 🌬️↙4mph 🌓 Tue Feb 28 08:49:25 2023
#W9Q1 – 59 ➡️ 305 – 293 ❇️ 71

import os
import time
import sys
import json
import requests
from config import log, HISTORY_FILE, OVERALL_RATE, COMPLICE_TOKEN, COMPLICE_CHECK, COMPLICE_INTENTION, SPRINT_DUR, OBSIDIAN_CHECK, OBSIDIAN_DAILY, OBSIDIAN_VAULT_PATH


myTimeStart = round(time.time())
Email_Start = sys.argv[1]
Email_StartF = f"{int(Email_Start):,}"

def sweepCounter(historyDict):

    # Get today's date in Unix format
    today_unix = int(time.time()) // 86400 * 86400

    # Count the number of timestamps in the dictionary that are from today
    myCount = 0
    for timestamp in historyDict.keys():
        if int(timestamp) >= today_unix:
            myCount += 1

    return myCount

    



from subprocess import Popen, PIPE, run




############
# COMPLICE SECTION ###
############

def get_emailZID(intention):
    
    url= 'https://intend.do/api/v0/u/me/today/core.json?auth_token='+COMPLICE_TOKEN 
    resp = requests.get(url)
    
    myResponse =  (resp.json())
    intentions = myResponse['list']
    
    myZID = ''
    for xx in intentions:
        if f"{xx['_c']}) {xx['t']}" == intention:
            myZID = xx["zid"]
            break
    
    return myZID
    

def post_intention(intention):
    
    url = 'https://intend.do/api/v0/u/me/intentions?auth_token='+COMPLICE_TOKEN 
    datastring = dict()
    
    datastring['raw'] = intention
    datastring['response'] = "today"
    
    resp = requests.post(url,data=datastring)
    
    myResponse =  (resp.json())
    intentions = myResponse['core']['list']
    myZID = ''
    for xx in intentions:
        if xx["t"] == intention:
            myZID = xx["zid"]
            break
    
    return myZID
    
    
    
def addPomo(zid,dur):
    url = 'https://intend.do/api/v0/u/me/add_dur?auth_token='+COMPLICE_TOKEN 
    datastring = {}
    datastring ['ty'] = 'sand'
    datastring ['min'] = dur
    datastring ['zidToAssignTo'] = zid
    resp = requests.post(url,data=datastring)


def fetchDailyNoteName():
    # Get today's date

    current_time = time.localtime()

    # Format today's date according to OBSIDIAN_DAILY
    myDailyNote = time.strftime(OBSIDIAN_DAILY, current_time)
    
    return myDailyNote

def main ():

    sprintDurSec = str(int(SPRINT_DUR) * 60)
    scpt = '''
        on run {sprintDur, Email_Start, Email_StartF, sprintDurSec}
            display notification ("Starting " & sprintDur & "-min sprint 💪.. GO!") with title (Email_StartF & " emails to clear") subtitle (sprintDur & " min sprint") sound name "Frog"

                
            tell application "Menubar Countdown"
        
                set hours to 0
                set minutes to sprintDur
                set seconds to 0
                set play alert sound to false
                set repeat alert sound to false
                set show alert window to false
                set show notification to false
                set play notification sound to false
                set speak announcement to false
                start timer
        
            
            delay (sprintDurSec as integer)
            
                stop timer
                end tell

            
            tell application "Microsoft Outlook"
                set mailAccount to first exchange account
                set InboxCount to (count messages in folder "Inbox" of mailAccount)
            end tell
            set mySwept to (Email_Start - InboxCount)
            set mySweepRate to (mySwept / sprintDur)
            set mySweepRate to ((round (mySweepRate * 100)) / 100)
            display dialog ("" & mySwept & " emails swept from " & Email_StartF & "\nCurrent 📬 count: " & InboxCount & "\nSweep rate: " & mySweepRate & "/min") with title "Mailstrom report" buttons {"OK"} default button "OK" giving up after 10 with icon POSIX file ("icon.png" as string)
            return {InboxCount, mySwept}
        end run'''

    args = [SPRINT_DUR, Email_Start, Email_StartF, sprintDurSec]
            
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(scpt)
    log (stdout)

    myResults = stdout.split(",")

    Email_End  = int(myResults[0])
    Email_Swept  = int(myResults[1])


    myTimeEnd = round(time.time())

    main_timeElapsed = round (myTimeEnd - myTimeStart)
    log (f"time elapsed: {main_timeElapsed}")

    ##############################
    #### WRITING DOWN HISTORY #####
    ##############################

    if not os.path.exists(HISTORY_FILE):
        mySweepHistory = {}
    else: 
        f = open(HISTORY_FILE)
        mySweepHistory = json.load(f)
        f.close()


    currentRun = {}
    currentRun['Email_Start'] = int(Email_Start)
    currentRun['Email_End'] = Email_End
    currentRun['Email_Swept'] = Email_Swept
    currentRun['main_timeElapsed'] = main_timeElapsed
    currentRun['myTimeStart'] = myTimeStart
    currentRun['myTimeEnd'] = myTimeEnd
    if Email_Swept == 0:
        currentRun['SweepRate'] = ''
    else:
        currentRun['SweepRate'] = round(Email_Swept/int(SPRINT_DUR),2)

    mySweepHistory[myTimeStart] = currentRun

    file2 = open(HISTORY_FILE, "w") 
    file2.write(json.dumps(mySweepHistory, indent = 4))
    file2.close()

    overallRate = sum([mySweepHistory[timestamp]['SweepRate'] for timestamp in mySweepHistory if mySweepHistory[timestamp]['SweepRate'] != ""]) / len([mySweepHistory[timestamp]['SweepRate'] for timestamp in mySweepHistory if mySweepHistory[timestamp]['SweepRate'] != ""])
    log (overallRate)

    file2 = open(OVERALL_RATE, "w") 
    file2.write(str(f"{overallRate:.2f}"))
    file2.close()


    sweepCount = sweepCounter(mySweepHistory)

    # copying report to clipboard

    myTimeStartF = time.strftime('%Y-%m-%d-%a, %I:%M', time.localtime(myTimeStart))
    myTimeEndF = time.strftime('%I:%M %p', time.localtime(myTimeEnd))


    reportString = f"""# Mailstrom {SPRINT_DUR}-min sprint ({sweepCount})
- {myTimeStartF}-{myTimeEndF}
- {Email_Swept} emails swept, from {Email_StartF} to {Email_End}
- Sweep rate: {currentRun['SweepRate']:.2f}, overall sweep rate: {overallRate:.2f}/min"""

    # Copy the string to the clipboard
    run('pbcopy', universal_newlines=True, input=reportString)

    if COMPLICE_CHECK == "1":
        myZID = ''
        myZID = get_emailZID(COMPLICE_INTENTION)
        
        
        if myZID:
            addPomo(myZID,SPRINT_DUR)
        else:
            myZID = post_intention(COMPLICE_INTENTION)
            addPomo(myZID,SPRINT_DUR)

    if OBSIDIAN_CHECK == "1":
        myDailyNote = fetchDailyNoteName()
        with open(f"{OBSIDIAN_VAULT_PATH}/{myDailyNote}.md", "a") as file:
            file.write(f"\n\n{reportString}")
        


if __name__ == '__main__':
    main()








 

