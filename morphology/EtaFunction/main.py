import numpy
import sys
import os
import ConfigParser

def runIt(fileName): # ainda precisa incorpara petroRad rowc,colc nas chamadas a m.run
    configFile = ConfigParser.ConfigParser()
    configFile.read(fileName)
    singleFunction = EtaFunction.EtaFunction()
    
    m.run(path,fileName,maskFile,saveResult, saveFig=saveFig, clear=True, clip=clip, xtraID=xtraID)
        

    ############################################
    #     Main temporario:
if __name__ == "__main__":
    if len(sys.argv)!=1:
        print("Input File Needed!")
    print(sys.argv[1])
    runIt(sys.argv[1])
   
