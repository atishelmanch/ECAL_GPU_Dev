# ECAL_GPU_Dev
The purpose of this repository is to investigate the use of GPUs for ECAL reconstruction within CMSSW. 

## Setup

Some instructions [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/TriggerDevelopmentWithGPUs).

```
ssh -4 -Y <userName>@lxplus.cern.ch
ssh -f -N -D18080 cmsusr.cern.ch
ssh -o ProxyCommand='nc --proxy localhost:18080 --proxy-type socks5 %h %p' gpu-c2a02-39-01.cms
mkdir /data/user/$USER
cd /data/user/$USER 
```

Available machines:

```
gpu-c2a02-37-03.cms
gpu-c2a02-37-04.cms
gpu-c2a02-39-01.cms
gpu-c2a02-39-02.cms
gpu-c2a02-39-03.cms
gpu-c2a02-39-04.cms
```

To use local releases of CMSSW:

```
export SCRAM_ARCH=slc7_amd64_gcc10
source /data/cmssw/cmsset_default.sh
scram list CMSSW
cmsrel <CMSSW_version>
```

To use CVMFS releases: 

```
export SCRAM_ARCH=slc7_amd64_gcc10
export CMS_PATH=/data/cmssw
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel <CMSSW_Version>
```

Test that git works:
```
ssh -T github.com
```

Running tests: 

```
cd CMSSW_12_3_0_pre5
cmsenv
mkdir run
cd run
runTheMatrix.py -w upgrade -l 11634.514
cmsRun step3_RAW2DIGI_RECO_custom.py userMaxEvents=10000 WithGPURecHits=0
cmsRun step3_RAW2DIGI_RECO_custom.py userMaxEvents=10000 WithGPURecHits=1
python GetTimes.py --inputFiles Resources_WithoutGPURecHits_NEvents_10000.json,Resources_WithGPURecHits_NEvents_10000.json
```

These final two tests should produce two output files. 

## Extra commands 

To check the current machine users `w`. To get associated job IDs for your user sessions: `ps -fu <userName>`. Kill an old session with: 

```
kill -9 <jobID>
```

