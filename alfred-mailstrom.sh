#!/bin/zsh

myOverallRateFile="$HOME/Library/Application Support/Alfred/Workflow Data/$alfred_workflow_bundleid/overallRate.txt"
if [ ! -f "$myOverallRateFile" ]
then
    myOverallRate=1
else
    myOverallRate=$(<"$myOverallRateFile")
	#myOverallRate=1
fi


#checking if the timer is running or paused
checkRun=$(osascript -e 'on run argv 
tell application "Menubar Countdown"
	if timer is paused then
        set myTime to (time remaining as text)
            if (myTime > 0) then
                return {"paused", myTime}
            end if
    else
        set myTime to (time remaining as text)
            if (myTime > 0) then
                return ("running " & myTime)
            end if
    end if
end tell
end run')


if [[ ${checkRun:+1} ]] ; then

    set -- $checkRun

    #if running or paused (time left): show how much is left with refresh
    if [ $2 -gt 0 ]
    then
        myMinutes=$(($2 / 60 )) 
        cat << EOX


            {"rerun": 1, "items": [


            {
                "title": "Active sprint $1, $myMinutes min ($2 sec) left",
                "subtitle": "↩️ to start a $sprintDur min 🧹 sprint, current rate: $myOverallRate/min",
                "arg": "",
                "icon": {
                    "path": "icon.png"
                    }	    
            },



            ]}
EOX

fi 

else



myOutput=$(osascript -e 'on run argv 
tell application "Microsoft Outlook"
set mailAccount to first exchange account
set InboxCount to (count messages in folder (item 1 of argv) of mailAccount)        
end tell
end run' $WatchFolder)
 
export LC_ALL=en_US.UTF-8 # need to change the locale to get the thousand separator to work!!
printf -v myFormatCount "%'.0d" $myOutput
pomoEstimate=$(echo "scale=1; $myOutput/$myOverallRate" | bc)
#pomoEstimate=$((myOutput/myOverallRate))
#printf -v pomoEstimateF "%'.1f" $pomoEstimate


cat << EOB


	{"items": [


    {
        "title": "You have $myFormatCount emails in $WatchFolder 📬 $pomoEstimate sprints needed @ $myOverallRate/min",
        "subtitle": "↩️ to start a $sprintDur min 🧹 sprint",
        "arg": $myOutput,
        "icon": {
			"path": "icon.png"
			}	    
	},



	]}
EOB

fi