"""
This is a testing version.
Run within the folder that contains Slack output.
Ex: TestEnvironment2022 Slack export May 31 2022 - June 1 2022
The output will be in a .txt file with a list of URLs per channel
per day.
Two categories: URLs Found is for urls that are not in
the list of socials. Held URLs for urls that are likely socials
or internal slack links that won't be available when the Slack
closes.
"""
import json
import os
import re
from pathlib import Path

# TODO Set up a way to take input or use working directory perhaps a toggle option?

parentFolder = Path.cwd()
slackOutFile = open(Path.cwd() / "SlackOutput.txt", 'a')
gandalfHeld = {}
gandalfReviewed = {}


def print_to_file(heldurls, reviewedurls):
    slackOutFile.write(f"--{'----' * 8}\n")
    slackOutFile.write(f"{'----' * 3}Found URLS{'----' * 3}\n")
    for i in reviewedurls:
        slackOutFile.write(f"--{'----' * 8}\n")
        slackOutFile.write(f'Channel: {i}\n')
        for x in reviewedurls[i]:
            slackOutFile.write(f'\t\t{x}\n')

    slackOutFile.write(f"--{'----' * 8}\n")
    slackOutFile.write(f"{'----' * 3}-Held URLS{'----' * 3}\n")

    for i in heldurls:
        slackOutFile.write(f"--{'----' * 8}\n")
        slackOutFile.write(f'Channel: {i}\n')
        for y in heldurls[i]:
            slackOutFile.write(f'\t\t{y}\n')
    slackOutFile.write(f"--{'----' * 8}\n")


def analyze_files(filename, subfolder):  # takes the argument from below (z) as filename
    allURLs = []
    with open(filename) as hallwayData:
        data = json.load(hallwayData)
        print(f"Taking URLs from file: {filename.name}")
        for d in data:  # passing list item (dict) to function findURL
            try:
                x = d['blocks'][0]['elements'][0]['elements'][0]['url']  # Is it ugly? Yes. Does it work? Also yes.
                allURLs.append(x)
            except KeyError or TypeError:  # no URL, no block
                pass
            try:
                y = d['files'][0]['external_url']
                allURLs.append(y)
            except KeyError or TypeError:  # no files, no URL
                pass

        toHoldURLs = []
        sortName = str(subfolder + " from " + filename.name[:-5])
        print(f"URls found: {len(allURLs)}")
        for i in allURLs:
            holdItems = re.compile('^(.*)(twitter|linkedin|imgur|giphy|tenor|slack)(.*)$')
            if holdItems.search(i):  # search the item in the list for the regex above
                toHoldURLs.append(i)  # if the item is found copy it to held and
                allURLs.remove(i)  # remove it from all

        if len(allURLs) >= 1:  # if what is left is more than one URL
            gandalfReviewed[sortName] = allURLs  # add it to gandalf
        if len(toHoldURLs) >= 1:  # same as above, give it to gandalf
            gandalfHeld[sortName] = toHoldURLs
        print("-----------------")  # This just makes it pretty


# Is this folder the right folder? Does it contain what you want? If yes, then proceed. (No validation checks yet)
def folder_check():
    for foldername, subfolders, filenames in os.walk(parentFolder):  # walk the folders/files in the parent folder
        print(f"Working with files in {foldername}...")  # announce the files we're working with
        for filename in filenames:  # for the files in the folders
            y = foldername  # store the actual file path
            x = Path(y).stem
            jsonOnly = re.compile('^(\d){4}-(\d){0,2}-(\d){0,2}(\.json)$')
            if jsonOnly.search(filename):  # search the item in the list for the regex above
                z = Path(y) / filename  # recreates the full path
                analyze_files(z, x)  # passes the full path up to the analyze_files function

                # TODO Option to exclude Business card channel


folder_check()  

print_to_file(gandalfHeld, gandalfReviewed)
slackOutFile.close()
