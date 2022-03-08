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

ECAL_modules = ["ecalMultiFitUncalibRecHitGPU", "EcalRawToDigiGPU"]
parameters = ["time_real"]
Uncommented_ECAL_modules = ["EcalUncalibRecHitProducerGPU", "EcalRawToDigiGPU"]

#Markdown_Table = """
#| file   | ecalMultiFitUncalibRecHitGPU real time | EcalRawToDigiGPU real time|
#|---|---|---|
#"""

#Markdown_Table = """
#| file   |EcalRawToDigiGPU real time|
#|---|---|
#"""

Markdown_Lines = []
Markdown_Lines.append("| file   |EcalRawToDigiGPU real time| EcalUncalibRecHitProducerGPU real time|")
Markdown_Lines.append("|---|---|---|")

for inputFile in inputFiles:
  with open(inputFile, "r") as f:
    print("file:",inputFile)
    file_info = json.load(f)
    modules = file_info["modules"]
    #print("modules:",modules)    
    #print(modules["ecalMultiFitUncalibRecHitGPU"][0])
    #print(modules["ecalMultiFitUncalibRecHitGPU"]["time_real"])
    #time_1 = float(modules["ecalMultiFitUncalibRecHitGPU"]["time_real"])
    for module in modules:
      moduleType = module["type"]
      print("moduleType:",moduleType)
      if(moduleType == "ecalMultiFitUncalibRecHitGPU"):
        time_1 = module["time_real"]
      elif(moduleType == "EcalRawToDigiGPU"):
        time_2 = module["time_real"]
      elif(moduleType == "EcalUncalibRecHitProducerGPU"):
        time_3 = module["time_real"]
    #time_2 = float(modules["EcalRawToDigiGPU"]["time_real"])
    #Markdown_Line = "|{inputFile}|{time_1}|{time_2}|".format(inputFile=inputFile, time_1=time_1, time_2=time_2)
    print("time_2:",time_2)
    print("time_3:",time_3)
    Markdown_Line = "|{inputFile}|{time_2}|{time_3}|".format(inputFile=inputFile, time_2=time_2, time_3=time_3)
    Markdown_Lines.append(Markdown_Line)
    #Markdown_Table.append("\n"+Markdown_Line)
    #print("modules:",modules)
    #for module in modules:
      #moduleType = module["type"]
      #if("Ecal" in moduleType):
        #print("")
        #print("ECAL module:",moduleType)
        #print(module)
    f.close()

Markdown_Table = "\n".join(Markdown_Lines)
print(Markdown_Table)


