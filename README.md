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

Running tests: 

```
cd CMSSW_12_3_0_pre5
cmsenv
mkdir run
cd run
runTheMatrix.py -w upgrade -l 11634.514
```
