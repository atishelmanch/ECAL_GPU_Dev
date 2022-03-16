"""
23 February 2022 
Abraham Tishelman-Charny 

The purpose of this python module is to extract times from CMSSW time report jsons.

Example usage:
python CompareCPUGPU_ECALRecHitWFs.py --inputFiles TimeReports/Resources_WithoutGPURecHits_NEvents_25000.json,TimeReports/Resources_WithGPURecHits_NEvents_25000.json
"""

import json 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inputFiles", type = str, required = True, help = "Input json file")
parser.add_argument("--verbose",action="store_true", help = "extra printouts for humans")
parser.add_argument("--timeVar", type = str, required = False, default = "time_real", help = "Time variable to get from timing report")
args = parser.parse_args()

verbose = args.verbose
inputFiles = args.inputFiles.split(",")
time_var = args.timeVar
print("Input files:",inputFiles)

LabelsToGetDict = {
  "WithGPURecHits" : ["ecalRecHit@cuda", "ecalRecHitGPU", "ecalRecHitSoA"], 
  "WithoutGPURecHits" : ["ecalMultiFitUncalibRecHitSoA", "ecalRecHit", "ecalRecHit@cpu", "ecalMultiFitUncalibRecHit@cuda"]
}

Markdown_Lines = []
#Markdown_Lines.append("| file   |EcalRawToDigiGPU real time| EcalUncalibRecHitProducerGPU real time|")
#Markdown_Lines.append("|file|")
Markdown_Lines.append("|---|---|---|")

for inputFile in inputFiles:
  with open(inputFile, "r") as f:
    print("file:",inputFile)
    totalPathTime = 0
    for ConfigType in LabelsToGetDict.keys():
      if(ConfigType in inputFile):
        LabelsToGet = LabelsToGetDict[ConfigType]
        print("module labels to get times for:",LabelsToGet)
    file_info = json.load(f)
    modules = file_info["modules"]
    for module in modules:
      label = module["label"]
      labelVarName = label.replace("@","at")
      if(verbose): print("label:",label)
      if(label in LabelsToGet):
        exec("%s_time = float(module[time_var])"%(labelVarName))
        exec("print('%s_time:',%s_time)"%(labelVarName, labelVarName))
        exec("totalPathTime += %s_time"%(labelVarName))
  print("TotalPathTime:",totalPathTime)

