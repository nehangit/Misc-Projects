#!/usr/bin/env python
#-------------------------------------------------------------------------------#
# Name:        spectAndCamFINAL.py                                              |
# Purpose:     heliCam LabView Integration                                      |
# Author:      Nehan Tarefder                                                   |
# Last update: 4/24/2023                                                        |
#-------------------------------------------------------------------------------#
from __future__ import division,print_function
import sys                            
import numpy as np
#import time
#import matplotlib.pyplot as plt

# import wrapper
sys.path.insert(0,r'C:\Program Files (x86)\Heliotis\heliCam\Python\wrapper') # make x32?
from libHeLIC import *

#-------------------------------------------------------------------------------#   Cam code begins here

def CamInit(DdsGain, SensTqp, SensNFrames, bs, SensNavM2):
# input cam settings
  global numFrames
  numFrames = SensNFrames
  cameraSettings = (
  ('AcqStop',1),
  ('SensNavM2',int(SensNavM2)),
  ('SensTqp',int(SensTqp)),            # add check for maximum value?
  ('SensNFrames',int(numFrames)),
  ('BSEnable',int(bs)),                # remove?
  ('DdsGain',int(DdsGain)),	           # change to actual gain value?
  ('InvEncCnt',0),
  ('CamMode',0),
  ('TrigFreeExtN',0),
  ('ExtTqp',1),
  ('OutEnDrv',1),
  ('EnTrigOnPos',0),
  ('AcqStop',0)
  )

# open camera
  global heSys
  heSys = LibHeLIC()
  heSys.Open(0,sys='c3cam_sl70') # open camera type SL70 (default)
# clear buffer ?
  res = 1        
  while res > 0:
    res = heSys.Acquire()

# set camera registers
  for k,v in cameraSettings:
    try:
      setattr(heSys.map,k,v)
    except RuntimeError:
      print('Could not set map property %s to %s',k,v)
# allocate data and timeout
  heSys.AllocCamData(1,LibHeLIC.CamDataFmt['DF_I16Q16'],0,0,0) # allocate memory by acquisition mode
  heSys.SetTimeout(60000) # set timeout in milliseconds

# time.sleep(1)

# get the offset acquisition
  global offsetI
  global offsetQ  
  res = heSys.Acquire()   
  res = heSys.Acquire()   

  res = heSys.Acquire()
  #print(res) 
  cd=heSys.ProcessCamData(1,0,0)
  meta = heSys.CamDataMeta()
  img=heSys.GetCamData(1,0,ct.byref(meta))
  data=img.contents.data
  data=LibHeLIC.Ptr2Arr(data,(int(numFrames),300,300,2),ct.c_ushort)
  dataI = data[:,:,:,0]
  dataQ = data[:,:,:,1]
  offsetI = dataI.mean(axis=0)
  offsetQ = dataQ.mean(axis=0)

def CamAcq():       # (startX, stopX, startY, stopY)
# get heliCam data
  #print("acq")
  res = heSys.Acquire()   
  cd=heSys.ProcessCamData(1,0,0)
  meta = heSys.CamDataMeta()
  img=heSys.GetCamData(1,0,ct.byref(meta))
  data=img.contents.data
  data=LibHeLIC.Ptr2Arr(data,(int(numFrames),300,300,2),ct.c_ushort) # convert data for python
  dataI = data[:,:,:,0]
  dataQ = data[:,:,:,1]
  meanI = dataI.mean(axis=0)        # isolate I and Q and get averages of frames
  meanQ = dataQ.mean(axis=0)


# subtract offset and calculate amplitude
  #meanI = meanI - offsetI
  #meanI = meanI.absolute()
  #meanQ = meanQ - offsetQ
  amp = np.sqrt(np.add(np.square(meanI), np.square(meanQ)))
  #amp = amp[int(startX):int(stopX),int(startY):int(stopY)]  # check if this still works?
  #amp = amp.astype(int)
  print(amp[100,200])
  print("meanI pixel: "+ str(meanI[100,200]))
  print("offsetI pixel: "+ str(offsetI[100,200]))

  #return amp                               # return meanI or amp as integer?
  #return meanI
  #return offsetI

# we can also append amplitude volumes to a global variable and return it at the end of the session for less data transfer?
# test amplitude mode of camera?
 

# exit
def CamExit():  # is this function call needed?
  setattr(heSys.map,'OutEnDrv',0)
  heSys.Close()
  #heSys.OpenDlgRegDesc(0)
  #dd = numpy.concatenate([mean I, meanQ])
  #print(str(dd.shape))  numpy 3D array

#-------------------------------------------------------------------------------------------------

# run (by labview)

CamInit(0, 2000, 150, 0, 50)

for i in range(5): # Note: the loop shifts the data somehow, after initializing the first and second acquisitions are always the same
  CamAcq()

CamExit()

# see command list for more spectrometer commands