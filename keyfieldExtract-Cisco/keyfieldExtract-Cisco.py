"""
.SYNOPSIS
  A program which extracts key fields from Cisco running configs and outputs them into CSV files.
  
.DESCRIPTION
  Digests lines from input file and exports key-fields data into individual .CSV files and merges them together. 
  Currently only searches for files in current directory
  Improvments to be made is to search for files withing subfolders
  
.PARAMETER <Parameter_Name>
  None
    
.INPUTS
  /*-config (Currently only searches in current directory)
  
.OUTPUTS
  ./*-config.csv
  ./keyfieldMerged.csv
  
.NOTES
  Version:        2.01
  Author:         Dennis Ozmert
  GitHub:         https://github.com/dozmert1
  Creation Date:  27/09/2021 @ 9:00am
  Last Updated:   19/11/2021
  Purpose/Change: Device config backup/discovery
  License:        GNU General Public License
  
.EXAMPLE
  .\keyfieldExtract-Cisco.py
 
.CITED WORK
  lutz, https://stackoverflow.com/questions/954504/how-to-get-files-in-a-directory-including-all-subdirectories
  unknown, https://www.pythontutorial.net/python-basics/python-write-csv-file/
"""
# --------------------------------------------------
## Imports and values
#
import os
import csv
import socket
#
dataDigestHostlist = []
workingDir = os.getcwd()
dataOutputName = 'keyfieldMerged'
print(workingDir)
#section below will need ot be adjusted for additional key-fields to be found. Add a new entry for a new option to search for.
dataMarkerHostname0 = 'hostname '
dataMarkerHostname1 = 'switchname'
#dataMarkerIP = 0 # managment IP capture curently unused.
dataMarkerNTP = 'ntp server'
dataMarkerDNS = 'ip name-server'
dataMarkerRAD1 = 'radius server'
dataMarkerRAD1Nexus = 'radius-server' # Used by cisco-nexus devices
dataMarkerRAD2 = 'address ipv4' # Note May capture more than RADIUS server IPs

# --------------------------------------------------
## Functions
#
def inputFilelist():
    for dirPath, dirNames, fileNames in os.walk('.'):
        for fileName in [f for f in fileNames if f.endswith('-confg')]: #Files ingested should have no file-extension
            # print (os.path.join(dirPath, fileName))
            # print(dirPath)
            # print(fileName)
            dataDigestHostlist.append(fileName) #Creates list of confg files to digest through
    #print('Digested files',dataDigestHostlist)
    print('Files acknowledged...')
#
def inputDigest(): #Steps through input file and checks for digestable data
    for confg in dataDigestHostlist:
        with open(str(confg)) as f0:
            with open(str(confg)+'.csv','w+',encoding='UTF8') as csv0: #Creation of individual CSV files
                csvWriteFile = csv.writer(csv0)
                csvHeader = ['Hostname','DNS','NTP','RADIUS'] #,'Managment IP','Legacy Commands'] #Headers in individual CSV files. This needs to be modified for additional key-fields to be contained in
                csvWriteFile.writerow(csvHeader)
                csvWriteFile.writerow('\n')
                #section below will need to be adjusted for additional key-fields to be contained in. Add a new entry for a new container to append to
                csvDataALL = []
                csvDataHOST = []
                csvDataDNS = []
                csvDataNTP = []
                csvDataRAD = []
#                csvDataIP = [] # Managment IP capture currently unused
                csvDataDNSsearch = []
                # If statments need to be copy-pasted for additional key-fields to appent to containers.
                for i0 in f0:
                    i1 = i0.replace('\n','') #Strips newline formatting from current digested line.
                    if dataMarkerHostname0 in i1 or dataMarkerHostname1 in i1:
                        maskMarker = i1.split(' ')
                        try:
                            csvDataHOST.append(maskMarker[1]) #Append hostname
                        except:
                            csvDataHOST.append('Null')
                            continue
#                        try: # Managment IP capture currently unused
#                            deviceIP = socket.gethostbyname(maskMarker[1])
#                            csvDataIP.append(deviceIP)
#                        except:
#                            csvDataIP.append('Null')
#                            continue    
                    if dataMarkerNTP in i1:
                        try:
                            csvDataNTP.append(i1)
                        except:
                            csvDataNTP.append('Null')
                            continue
                    if dataMarkerDNS in i1:
                        try:
                            csvDataDNS.append(i1)
                        except:
                            csvDataDNS.append('Null')
                            continue
                    if dataMarkerRAD1 in i1:#
                        try:
                            csvDataRAD.append(i1)
                        except:
                            csvDataRAD.append('Null')
                            continue
                    if dataMarkerRAD1Nexus in i1: # For Cisco-nexus devices
                        try:
                            csvDataRAD.append(i1)
                        except:
                            csvDataRAD.append('Null')
                            continue
                    if dataMarkerRAD2 in i1:
                        try:
                            csvDataRAD.append(i1)
                        except:
                            csvDataRAD.append('Null')
                            continue
                csvDataALL = [csvDataHOST,csvDataDNS,csvDataNTP,csvDataRAD] #,csvDataIP] # Managment IP capture currently unused.
                print(csvDataALL,'\n')
                csvWriteFile.writerow(csvDataALL,) # Writes containers to individual CSV files.
                csvWriteFile.writerow('\n')
    print('Files digested into CSV...')
#
def outputMerge():
    os.system('copy *.csv '+dataOutputName+'.csv') #Executes CMD to 'manually' merge CSV files. Currently works on :C drive files.
# --------------------------------------------------
## Code start
#
print('Program start...')
inputFilelist()
inputDigest()
outputMerge()
print('Program ending.')
# --------------------------------------------------