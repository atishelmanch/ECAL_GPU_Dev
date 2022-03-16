"""
16 March 2022
Abraham Tishelman-Charny 

The purpose of this CMSSW configuration file is to run offline reconstruction with ECAL rec hits produced on CPUs vs. GPUs to determine the differences in run time and energy reconstruction, 
in order to check if GPUs can be used to speed up reconstruction time, while making sure energy values are not affected.
"""

# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 -s RAW2DIGI:RawToDigi_ecalOnly,RECO:reconstruction_ecalOnly --conditions auto:phase1_2021_realistic --datatier GEN-SIM-RECO,DQMIO -n 10 --eventcontent RECOSIM,DQM --geometry DB:Extended --era Run3 --procModifiers gpu --customise RecoLocalCalo/Configuration/customizeEcalOnlyForProfiling.customizeEcalOnlyForProfilingGPUOnly --filein file:step2.root --fileout file:step3.root

import os 
import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.ProcessModifiers.gpu_cff import gpu

process = cms.Process('RECO',Run3,gpu)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# custom aguments 
from ConfigParams import options 

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.userMaxEvents),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# some customization to add timing 

process.load('HLTrigger.Timer.FastTimerService_cfi')
process.FastTimerService.enableDQM = False
process.FastTimerService.printRunSummary = False
process.FastTimerService.printJobSummary = True
process.FastTimerService.writeJSONSummary = True

WithGPURecHits = options.WithGPURecHits

print("With ECAL GPU rec hits:",WithGPURecHits)

# Determine names for output files based on configuration parameters 
outGPULabelDict = {
  0 : "WithoutGPURecHits",
  1 : "WithGPURecHits",
}

outTimeDirec = "TimeReports"
outAnalyzerDirec = "AnalyzerOutputs"

# create output directories if they don't already exist 
if(not os.path.isdir(outTimeDirec)): os.system("mkdir -p %s"%(outTimeDirec))
if(not os.path.isdir(outAnalyzerDirec)): os.system("mkdir -p %s"%(outAnalyzerDirec))

outGPULabel = outGPULabelDict[WithGPURecHits]
outJsonName = "%s/Resources_%s_NEvents_%s.json"%(outTimeDirec, outGPULabel, options.userMaxEvents)
outRecoName = "%s/step3_%s_NEvents_%s.root"%(outAnalyzerDirec, outGPULabel, options.userMaxEvents)
outDQMName = "%s/step3_inDQM_%s_NEvents_%s.root"%(outAnalyzerDirec, outGPULabel, options.userMaxEvents)

process.FastTimerService.jsonFileName = outJsonName
process.MessageLogger.FastReport = cms.untracked.PSet()
process.options.wantSummary = True

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:step2.root'),
    secondaryFileNames = cms.untracked.vstring()
)


if(options.overrideSource):
  print("Overriding input files with source_cff")
  process.load( "source_cff" )

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RECO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:%s'%(outRecoName)),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:%s'%(outDQMName)),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi_ecalOnly)
process.reconstruction_step = cms.Path(process.reconstruction_ecalOnly)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.RECOSIMoutput_step,process.DQMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

#if(options.overrideSource): 
#  print("Overriding input files with source_cff")
#  process.load( "source_cff" )


#print("process.RECOSIMoutput_step:",process.RECOSIMoutput_step)

# Automatic addition of the customisation function from RecoLocalCalo.Configuration.customizeEcalOnlyForProfiling
#from RecoLocalCalo.Configuration.customizeEcalOnlyForProfiling import customizeEcalOnlyForProfilingGPUOnly 
from RecoLocalCalo.Configuration.customizeEcalOnlyForProfiling import customizeEcalOnlyForProfiling 

#call to customisation function customizeEcalOnlyForProfilingGPUOnly imported from RecoLocalCalo.Configuration.customizeEcalOnlyForProfiling
#process = customizeEcalOnlyForProfilingGPUOnly(process)
process = customizeEcalOnlyForProfiling(process)

if(WithGPURecHits):
  print("Setting ECAL Rec hit computation to use GPUs")
  #process.load("RecoLocalCalo.EcalRecProducers.ecalRecHit_cff")
  
  from RecoLocalCalo.EcalRecProducers.ecalRecHitConvertGPU2CPUFormat_cfi import ecalRecHitConvertGPU2CPUFormat as _ecalRecHitFromSoA
  #from Configuration.ProcessModifiers.gpu_cff import gpu

  # ECAL calibrated rechit reconstruction on CPU
  from HeterogeneousCore.CUDACore.SwitchProducerCUDA import SwitchProducerCUDA 

  gpu.toModify(process.ecalRecHit,
    cuda = _ecalRecHitFromSoA.clone(
    recHitsLabelGPUEB = cms.InputTag('ecalRecHitSoA', 'EcalRecHitsEB'),
       recHitsLabelGPUEE = cms.InputTag('ecalRecHitSoA', 'EcalRecHitsEE')
    )
  )

print("removing crystal recovery to make CPU GPU comparisons more equal")
process.ecalRecHit.cpu.recoverEBFE = cms.bool(False)
process.ecalRecHit.cpu.recoverEEFE = cms.bool(False)
process.ecalRecHit.cpu.killDeadChannels = cms.bool(False)

# End of customisation functions

# Customisation from command line

process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( options.Printerval ) # Printout run, lumi, event info

if(options.ProduceOutputRoot): process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step, process.consume_step, process.RECOSIMoutput_step,process.DQMoutput_step)

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
