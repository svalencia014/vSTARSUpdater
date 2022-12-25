import json
from os.path import exists
import os
from pathlib import Path

import requests
from zipfile import ZipFile
import gzip
import glob

if (exists("C:\\vSTARSUpdater")):
    os.chdir("C:\\vSTARSUpdater")
else:
    os.mkdir("C:\\vSTARSUpdater")
    os.chdir("C:\\vSTARSUpdater")
config = input("What is the path of your config.json file? ")
if not config.endswith(".json"):
    exit(1)
configJson = json.load(open(config, "r"))

artccs = configJson["ARTCCs"]
facilities = {}

for artcc in artccs:
    facilities[artcc] = configJson[artcc]['Facilities']

print(facilities)

for key in facilities:
    path = "C:\\vSTARSUpdater\\" + key + "\\"
    if (exists(path)):
        print("ARTCC has been updated before")
    else:
        print("New ARTCC Detected")
        os.mkdir(path)

    for facility in facilities[key]:
        path += str(facility['Name']) + "\\"
        print(path)
        if (exists(path)):
            print("Profile has been updated before")
            f = open(path + "airac.txt", "r")
            airac = f.read()
            if str(airac) != str(configJson["Current"]): # Swap to == after testing
                print("Profile is up to date")
            else:
                print("Profile is out of date")

                url = str(facility['URL'])
                x = url.split("/")
                for i in x:
                    if i.__contains__(''):
                        x.remove(i)
                x = x[2]
                if x.__contains__('%20'):
                    x = x.replace('%20', '_')
                r = requests.get(url)
                open(path + x, "wb").write(r.content)

                if x.endswith(".zip"): # ZDC Does this cause they wierd
                    with ZipFile(path + x, 'r') as zipObj:
                        zipObj.extractall(path)
                    os.remove(path + x)
                    x = x.replace('.zip', '.gz')
                    y = str(glob.glob(path + '*.gz')).replace('[', '').replace(']', '').replace("'", '')
                else:
                    y = path + x

                #   Open GZ file
                with gzip.open(y, 'rb') as f:
                    file_content = f.read()
                    y = y.replace('.gz', '.xml')
                    open(y, "wb").write(file_content)
                print(x)

        else:
            print("New Profile Detected")
            os.mkdir(path)
            f = open(path + "airac.txt", "x")
            f.write("2212")
            f.close()
