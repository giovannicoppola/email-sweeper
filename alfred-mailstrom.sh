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



mailboxCount=$(osascript -e 'on run argv 
tell application "Microsoft Outlook"
set mailAccount to first exchange account
set InboxCount to (count messages in folder (item 1 of argv) of mailAccount)        
end tell
end run' $WatchFolder)
 
export LC_ALL=en_US.UTF-8 # need to change the locale to get the thousand separator to work!!
printf -v myFormatCount "%'.0d" $mailboxCount
pomoEstimate=$(echo "scale=1; ($mailboxCount/$myOverallRate)/$sprintDur" | bc)

totMinutesD=$(echo "$pomoEstimate * $sprintDur" | bc -l)
totMinutes=$(printf "%.0f" "$totMinutesD")


if [ $totMinutes -lt 60 ]; then
    formatMinutes="$totMinutesM"
elif [ $totMinutes -lt 1440 ]; then
    hours="$((totMinutes / 60))h:"
    minutes="$((totMinutes % 60))m"
    formatMinutes="$hours$minutes"
elif [ $totMinutes -lt 43800 ]; then
    days="$((totMinutes / 1440))d:"
    remainder=$((totMinutes % 1440))
    hours="$((remainder / 60))h:"
    minutes="$((remainder % 60))m"
    formatMinutes="$days$hours$minutes"
else
    months="$((totMinutes / 43800))mo:"
    remainder=$((totMinutes % 43800))
    days="$((remainder / 1440))d:"
    remainder=$((remainder % 1440))
    hours="$((remainder / 60))h:"
    minutes="$((remainder % 60))m"
    formatMinutes="$months$days$hoursH$minutes"
fi




cat << EOB


	{"items": [


    {
        "title": "You have $myFormatCount emails in $WatchFolder 📬 $pomoEstimate $sprintDur-min sprints ($formatMinutes) needed @ $myOverallRate/min",
        "subtitle": "↩️ to start a $sprintDur min sprint 🧹 ",
        "arg": $mailboxCount,
        "icon": {
			"path": "icon.png"
			}	    
	},



	]}
EOB

fi