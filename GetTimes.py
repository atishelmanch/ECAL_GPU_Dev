"""
23 February 2022 
Abraham Tishelman-Charny 

The purpose of this python module is to extract times from CMSSW time report jsons.
"""

import json 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inputFiles", type = str, required = True, help = "Input json file")
args = parser.parse_args()

inputFiles = args.inputFiles.split(",")

print("Input files:",inputFiles)

for inputFile in inputFiles:
  with open(inputFile, "r") as f:
    print("file:",inputFile)
    file_info = json.load(f)
    modules = file_info["modules"]
    #print("modules:",modules)
    for module in modules:
      moduleType = module["type"]
      if("Ecal" in moduleType):
        print("")
        print("ECAL module:",moduleType)
        print(module)
    f.close()
