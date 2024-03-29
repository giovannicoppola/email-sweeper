#!/usr/bin/env python3

import os
import sys

    

WF_BUNDLE = os.getenv('alfred_workflow_bundleid')
CACHE_FOLDER = os.path.expanduser('~')+"/Library/Caches/com.runningwithcrayons.Alfred/Workflow Data/"+WF_BUNDLE+"/"
DATA_FOLDER = os.path.expanduser('~')+"/Library/Application Support/Alfred/Workflow Data/"+WF_BUNDLE
HISTORY_FILE = f"{DATA_FOLDER}/sweepHistory.json"
OVERALL_RATE = f"{DATA_FOLDER}/overallRate.txt"

SPRINT_DUR = str(os.getenv('sprintDur'))
COMPLICE_CHECK = os.path.expanduser(os.getenv('COMPLICE_CHECK'))
COMPLICE_TOKEN = os.path.expanduser(os.getenv('COMPLICE_TOKEN'))
COMPLICE_INTENTION = os.path.expanduser(os.getenv('COMPLICE_INTENTION'))


if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(OVERALL_RATE):
    file2 = open(OVERALL_RATE, "w") 
    file2.write("1")
    file2.close()

            


def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


