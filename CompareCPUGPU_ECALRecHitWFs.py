"""
23 February 2022 
Abraham Tishelman-Charny 

The purpose of this python module is to extract times from CMSSW time report jsons.

Example usage:
python GetTimes.py --inputFiles Resources_WithoutGPURecHits_NEvents_10000.json,Resources_WithGPURecHits_NEvents_10000.json
"""

import json 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--inputFiles", type = str, required = True, help = "Input json file")
args = parser.parse_args()

inputFiles = args.inputFiles.split(",")

print("Input files:",inputFiles)

# if WithGPURecHits in inputFile
#  get ecalRecHit@cuda, ecalRecHitGPU, ecalRecHitSoA 
# if WithoutGPURecHits in inpuFile
#  get ecalMultiFitUncalibRecHitSoA, ecalRecHit, ecalRecHit@cpu

for inputFile in inputFiles:
  with open(inputFile, "r") as f:
    print("file:",inputFile)
    file_info = json.load(f)
    modules = file_info["modules"]
    #print("modules:",modules)    
    #print(modules["ecalMultiFitUncalibRecHitGPU"][0])
    #print(modules["ecalMultiFitUncalibRecHitGPU"]["time_real"])
    #time_1 = float(modules["ecalMultiFitUncalibRecHitGPU"]["time_real"])
    

    """
    for module in modules:
      moduleType = module["type"]
      print("moduleType:",moduleType)
      if(moduleType == "ecalMultiFitUncalibRecHitGPU"):
        time_1 = module["time_real"]
      elif(moduleType == "EcalRawToDigiGPU"):
        time_2 = module["time_real"]
      elif(moduleType == "EcalUncalibRecHitProducerGPU"):
        time_3 = module["time_real"]
    print("time_2:",time_2)
    print("time_3:",time_3)
    Markdown_Line = "|{inputFile}|{time_2}|{time_3}|".format(inputFile=inputFile, time_2=time_2, time_3=time_3)
    Markdown_Lines.append(Markdown_Line)
    f.close()

    """

#Markdown_Table = "\n".join(Markdown_Lines)
#print(Markdown_Table)
