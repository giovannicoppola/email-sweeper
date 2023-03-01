#!/usr/bin/python3 

## email Sprinter
# 
##  – Light snow, mist 🌨  🌡️+31°F (feels +22°F, 85%) 🌬️↙4mph 🌓 Tue Feb 28 08:49:25 2023
#W9Q1 – 59 ➡️ 305 – 293 ❇️ 71

import os
import time
import sys
import json
from config import log, HISTORY_FILE, OVERALL_RATE

myTimeStart = round(time.time())
Email_Start = sys.argv[1]
Email_StartF = f"{int(Email_Start):,}"

from subprocess import Popen, PIPE

sprintDur = str(os.getenv('sprintDur'))
sprintDurSec = str(int(sprintDur) * 60)
scpt = '''
    on run {sprintDur, Email_Start, Email_StartF, sprintDurSec}
        display notification ("Starting " & sprintDur & "-min sprint 💪") with title (Email_StartF & " emails to clear") subtitle (sprintDur & " min sprint") sound name "Frog"

               
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

        set the clipboard to "Some text"
        tell application "Microsoft Outlook"
        	set mailAccount to first exchange account
            set InboxCount to (count messages in folder "Inbox" of mailAccount)
        end tell
        set mySwept to (Email_Start - InboxCount)
        set mySweepRate to (mySwept / sprintDur)
        display dialog ("" & mySwept & " emails swept from " & Email_StartF & "\nCurrent 📬 count: " & InboxCount & "\nSweep rate: " & mySweepRate & "/min") with title "Mailstrom report" buttons {"OK"} default button "OK" giving up after 10 with icon POSIX file ("icon.png" as string)
        return {InboxCount, mySwept}
    end run'''

args = [sprintDur, Email_Start, Email_StartF, sprintDurSec]

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
    currentRun['SweepRate'] = Email_Swept/int(sprintDur)

mySweepHistory[myTimeStart] = currentRun

file2 = open(HISTORY_FILE, "w") 
file2.write(json.dumps(mySweepHistory, indent = 4))
file2.close()

overallRate = sum([mySweepHistory[timestamp]['SweepRate'] for timestamp in mySweepHistory if mySweepHistory[timestamp]['SweepRate'] != ""]) / len([mySweepHistory[timestamp]['SweepRate'] for timestamp in mySweepHistory if mySweepHistory[timestamp]['SweepRate'] != ""])
log (overallRate)

file2 = open(OVERALL_RATE, "w") 
file2.write(str(f"{overallRate:.2f}"))
file2.close()







 

