import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import norm
import pandas as pd
import math

#import rpy2.robjects as robject
#from pyper import *

import ConfigParser
import os
import sys
import fileinput

sExtractorParamFile1 = 'maskMaker/sextractor-2.19.5/config/default.sex'
sExtractorParamFile2 = 'default.sex'
desiredParam = 'DETECT_THRESH'

def getSeparatedClasses(datafile):
    dataset = pd.read_csv(datafile)
    fileE = 'optimize/optimize_input/early_type.csv'
    fileL = 'optimize/optimize_input/late_type.csv'
    resultE = dataset[(dataset['Zoo1class'] == 'E')]    
    resultE.to_csv(fileE, index=False)
    resultS = dataset[(dataset['Zoo1class'] == 'S')]
    resultS.to_csv(fileL, index=False)    
    return (fileE, fileL)

# distance metric from GPA paper (boxCounting)
def boxCountingDistance(data1, data2, metrica):
    hist1, bins1 = np.histogram(data1[metrica])
    hist2, bins2 = np.histogram(data2[metrica])
    both = np.concatenate((bins1,bins2))
    
    n = len(both)/2
    rnge = (np.min(both),np.max(both))
    hist1, bins1 = np.histogram(data1[metrica],bins=n,range=rnge,normed=True)
    hist2, bins2 = np.histogram(data2[metrica],bins=n,range=rnge,normed=True)
    
    dx = (rnge[1]-rnge[0])/n
    dy = np.minimum(hist1,hist2)

    ao = np.sum(dy*dx)

    a_height = np.max(hist1)
    b_height = np.max(hist2)
    c_height = np.max(dy)
    
    SepBCA = 1 - (ao) / (2.0 - ao)
    SepBCL = (a_height + b_height - 2.0 * c_height) / (a_height + b_height)

    SepMean = ( SepBCA + SepBCL ) / 2.0
    SepRoot = ( math.sqrt(SepBCA) + SepBCL ) / 2.0
    
    return [SepBCA, SepBCL, SepMean, SepRoot]

# distance metric from GPA paper (boxCounting) with K
def boxCountingDistanceK(k, data1, data2, metrica):
    hist1, bins1 = np.histogram(data1[metrica])
    hist2, bins2 = np.histogram(data2[metrica])
    both = np.concatenate((bins1,bins2))
    
    n = len(both)/2
    rnge = (np.min(both),np.max(both))
    hist1, bins1 = np.histogram(data1[metrica],bins=n,range=rnge,normed=True)
    hist2, bins2 = np.histogram(data2[metrica],bins=n,range=rnge,normed=True)
    
    dx = (rnge[1]-rnge[0])/n
    dy = np.minimum(hist1,hist2)

    ao = np.sum(dy*dx)

    a_height = np.max(hist1)
    b_height = np.max(hist2)
    c_height = np.max(dy)
    
    SepBCA = 1 - (ao) / (2.0 - ao)
    SepBCL = (a_height + b_height - 2.0 * c_height) / (a_height + b_height)

    SepMean = ( SepBCA + SepBCL ) / 2.0
    SepRoot = ( math.sqrt(SepBCA) + SepBCL ) / 2.0
    
    return [k, SepBCA, SepBCL, SepMean, SepRoot]

#python version(discrete suppervised):
def runMetric(r1,b1,idx):
    r = pd.read_csv(r1).dropna()
    b = pd.read_csv(b1).dropna()
    return boxCountingDistance(r,b,idx)

def runMetricK(k,r1,b1,idx):
    r = pd.read_csv(r1).dropna()
    b = pd.read_csv(b1).dropna()
    return boxCountingDistanceK(k,r,b,idx)

def runPCymorph(datafile,nprocess):
    cmd = "mpirun -np "+str(nprocess)+" PCyMorph.sh "+datafile
    cmd = "mpirun -np "+str(nprocess)+" python PCyMorph.py "+datafile
    process = os.popen(cmd)
    out = process.read()   

def optimizeCN(dataFile1,dataFile2, nprocess=2):
    if(nprocess<2):
        raise Exception("You must specify nprocess>1 (at least one headnode, and a worker)")
    r1_values = [0.55, 0.6, 0.65, 0.7, 0.75, 0.8]
    r2_values = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
    output_file = "optimize/conc.csv"
    # iterate over different values of metric parameters
    metrics = []
    for r1 in r1_values:
        for r2 in r2_values:
            print "Starting CN with (r1, r2) = ("+str(r1)+", "+str(r2)+")"
            print "Nprocess = "+str(nprocess)
            parser = ConfigParser.ConfigParser()
            parser.add_section("File_Configuration")
            parser.add_section("Output_Configuration")
            parser.add_section("Indexes_Configuration")
            parser.set("File_Configuration","Indexes","C")
            parser.set("Output_Configuration","Verbose",False)
            parser.set("Output_Configuration","SaveFigure",False)
            parser.set("Indexes_Configuration","Concentration_Distances",str(r1)+","+str(r2))
            parser.set("Indexes_Configuration","Concentration_Density",100)
            parser.set("File_Configuration","cleanit",False)
            parser.set("File_Configuration","download",False)
            parser.set("File_Configuration","band","r") ## Paulo_25-07-17
            
            with open("ParallelConfig.ini","w") as cfgfile:
                parser.write(cfgfile)
            cmd ="mpirun -np "+str(nprocess)+" PCyMorph.sh "+dataFile1
            process = os.popen(cmd)
            process.read()
            process = os.popen("mv output/result.csv output/r1.csv")
            process.read()
            cmd ="mpirun -np "+str(nprocess)+" PCyMorph.sh "+dataFile2
            process = os.popen(cmd)
            process.read()
            process = os.popen("mv output/result.csv output/r2.csv")
            process.read()
            print "Running boxCounting metric"
            try:
                nm = runMetric("output/r1.csv","output/r2.csv","CN")
                nm.insert(0,r1)
                nm.insert(0,r2)
                metrics.append(nm)
                df = pd.DataFrame(metrics)
                df.columns = ["r1","r2","SepBCA", "SepBCL", "SepMean", "SepRoot"]
                print(df)
                df.to_csv(output_file, index=False)
                process = os.popen("mkdir output/Cr"+str(r1)+"r"+str(r2))
                process.read()
                process = os.popen("mv output/r1.csv output/r2.csv output/Cr"+str(r1)+"r"+str(r2)+"/")
                process.read()
            except:
                print "Error with CN; r1 = "+str(r1)+"; r2 = "+str(r2)

def optimizeEntropy(hm,dataFile1,dataFile2, nprocess=2):
    if(nprocess<2):
        raise Exception("You must specify nprocess>1 (at least one headnode, and a worker)")
   
    # iterate over different values of metric parameters
    metrics = []
    # k_values = [0.8, 1.0, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    k_values = [0.1, 0.3, 0.5, 0.7]
    output_file = "optimize/entropy.csv"
    for hv in hm:
         # edit DETECT_THRESH for sExtractor
        for k in k_values:
            for line in fileinput.FileInput(sExtractorParamFile1, inplace=1):
                if not desiredParam in line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                        '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')
            for line in fileinput.FileInput(sExtractorParamFile2, inplace=1):
                if not desiredParam in line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                        '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')

            # hv = int(hm[0]+float(i)*(hm[1]-hm[0])/float(nsamples))
            print "Starting H = "+str(hv)+"; k = "+str(k)
            print "Nprocess = "+str(nprocess)
            parser = ConfigParser.ConfigParser()
            parser.add_section("File_Configuration")
            parser.add_section("Output_Configuration")
            parser.add_section("Indexes_Configuration")
            parser.set("File_Configuration","Indexes","H")

            parser.set("File_Configuration","cleanit",False)
            parser.set("File_Configuration","download",True)
            parser.set("File_Configuration","band","r") ## Paulo_25-07-17

            parser.set("Output_Configuration","Verbose",False)
            parser.set("Output_Configuration","SaveFigure",False)
            parser.set("Indexes_Configuration","Entropy_Bins",int(hv))
            with open("ParallelConfig.ini","w") as cfgfile:
                parser.write(cfgfile)
            runPCymorph(dataFile1,nprocess)
            process = os.popen("mv output/result.csv output/r1.csv")
            out = process.read()
            runPCymorph(dataFile2,nprocess)
            process = os.popen("mv output/result.csv output/r2.csv")
            process.read()
            print "Running boxCounting metric"
            try:
                nm = runMetricK(k, "output/r1.csv","output/r2.csv","sH")                
                nm.insert(0,hv)
                metrics.append(nm)
                df = pd.DataFrame(metrics)
                df.columns = ["H","k","SepBCA", "SepBCL", "SepMean", "SepRoot"]
                print(df)
                df.to_csv(output_file, index=False)
                process = os.popen("mkdir output/Entropy/Hbin"+str(hv)+"_k"+str(k))
                process.read()
                process = os.popen("mv output/r1.csv output/r2.csv output/Entropy/Hbin"+str(hv)+"_k"+str(k)+"/")
                process.read()
            except:
                print "Error with h = "+str(hv)+"; k = "+str(k)

def optimizeGa(gaTol,gaAngTol,dataFile1,dataFile2, nprocess=2):
    if(nprocess<2):
        raise Exception("You must specify nprocess>1 (at least one headnode, and a worker)")
 
    # iterate over different values of metric parameters
    metricsGa = []
    k_values = [0.1, 0.3, 0.5, 0.7, 0.8, 1.0, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    output_file = "optimize/ga.csv"
    for gaMTol in gaTol:
        # edit DETECT_THRESH for sExtractor
        for k in k_values:
            for line in fileinput.FileInput(sExtractorParamFile1, inplace=1):
                if not desiredParam in line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                        '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')
            for line in fileinput.FileInput(sExtractorParamFile2, inplace=1):
                if not desiredParam in line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                        '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')

            # gaMTol = round(gaTol[0]+float(i)*(gaTol[1]-gaTol[0])/float(nsamples),3)
            print "Starting Ga (Mod, Ang) = ("+str(gaMTol)+", "+str(gaAngTol)+"); k = "+str(k)
            print "Nprocess = " +str(nprocess)
            parser = ConfigParser.ConfigParser()
            parser.add_section("File_Configuration")
            parser.add_section("Output_Configuration")
            parser.add_section("Indexes_Configuration")
            parser.set("File_Configuration","Indexes","Ga")
            parser.set("Output_Configuration","Verbose",False)
            parser.set("Output_Configuration","SaveFigure",False)
            parser.set("File_Configuration","cleanit",False)
            parser.set("Indexes_Configuration","Ga_Tolerance",gaMTol)
            parser.set("Indexes_Configuration","Ga_Angular_Tolerance",gaAngTol)
            parser.set("Indexes_Configuration","Ga_Position_Tolerance",0.0)
            parser.set("File_Configuration","download",False)
            parser.set("File_Configuration","band","r") ## Paulo_25-07-17
            with open("ParallelConfig.ini","w") as cfgfile:
                parser.write(cfgfile)
            cmd ="mpirun -np "+str(nprocess)+" PCyMorph.sh "+dataFile1
            process = os.popen(cmd)
            process.read()
            process = os.popen("mv output/result.csv output/r1.csv")
            process.read()
            cmd ="mpirun -np "+str(nprocess)+" PCyMorph.sh "+dataFile2
            process = os.popen(cmd)
            process.read()
            process = os.popen("mv output/result.csv output/r2.csv")
            process.read()
            print "Running boxCounting metric"
            try:
                nm = runMetric("output/r1.csv","output/r2.csv","sGa")
                nm.insert(0,gaMTol)
                metricsGa.append(nm)
                df = pd.DataFrame(metricsGa)
                df.columns = ["Mod","k","SepBCA", "SepBCL", "SepMean", "SepRoot"]
                print(df)
                df.to_csv(output_file, index=False)
                process = os.popen("mkdir output/Ga"+str(gaMTol)+"_k"+str(k))
                process.read()
                process = os.popen("mv output/r1.csv output/r2.csv output/Ga"+str(gaMTol)+"_k"+str(k)+"/")
                process.read()
            except:
                print "Error with GaMTol = "+str(gaMTol)+"; k = "+str(k)

def optimizeSmoothness(sm,dataFile1,dataFile2, nprocess=2):
    # iterate over different values of metric parameters
    # metricsS2 = []
    metricsS3 = []    
    # k_values = [0.8, 1.0, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    k_values = [0.1, 0.3, 0.5, 0.7]
    # output_file_s2 = "optimize/s2.csv"
    output_file_s3 = "optimize/s3.csv"

    for cv in sm:
        # edit DETECT_THRESH for sExtractor
        for k in k_values:
            for line in fileinput.FileInput(sExtractorParamFile1, inplace=1):
                if not desiredParam in line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                        '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')
            for line in fileinput.FileInput(sExtractorParamFile2, inplace=1):
                if not desiredParam in line:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                else:
                    sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                        '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')
 
            # cv = round(sm[0]+float(i)*(sm[1]-sm[0])/float(nsamples),3)
            print "Starting Smoothness = "+str(cv)+"; k = "+str(k)
            print "Nprocess = "+str(nprocess)
            parser = ConfigParser.ConfigParser()
            parser.add_section("File_Configuration")
            parser.add_section("Output_Configuration")
            parser.add_section("Indexes_Configuration")
            parser.set("File_Configuration","Indexes","S")
            parser.set("Output_Configuration","Verbose",False)
            parser.set("Output_Configuration","SaveFigure",False)
            parser.set("Indexes_Configuration","smooth_degree",cv)
            parser.set("Indexes_Configuration","butterworth_order",2.0)
            parser.set("File_Configuration","cleanit",False)
            parser.set("File_Configuration","download",False)
            parser.set("File_Configuration","band","r") ## Paulo_25-07-17

            with open("ParallelConfig.ini","w") as cfgfile:
                parser.write(cfgfile)
            runPCymorph(dataFile1,nprocess)
            process = os.popen("mv output/result.csv output/r1.csv")
            out = process.read()  
            runPCymorph(dataFile2,nprocess)
            process = os.popen("mv output/result.csv output/r2.csv")
            process.read()
            print "Running boxCounting metric"
            # try:
            #     nm = runMetric("output/r1.csv","output/r2.csv","sS2")
            #     nm.insert(0,cv)
            #     metricsS2.append(nm)
            #     df = pd.DataFrame(metricsS2)
            #     df.columns = ["S2","k","SepBCA", "SepBCL", "SepMean", "SepRoot"]
            #     print(df)
            #     df.to_csv(output_file_s2, index=False)

            # except:
            #     print "Error with s2 = "+str(cv)+"; k = "+str(k)
            try:
                nm = runMetricK(k,"output/r1.csv","output/r2.csv","sS3")
                nm.insert(0,cv)
                metricsS3.append(nm)
                df = pd.DataFrame(metricsS3)
                df.columns = ["S3","k","SepBCA", "SepBCL", "SepMean", "SepRoot"]
                print(df)
                df.to_csv(output_file_s3, index=False)
                process = os.popen("mkdir output/S/S"+str(cv)+"_k"+str(k))
                process.read()
                process = os.popen("mv output/r1.csv output/r2.csv output/S/S"+str(cv)+"_k"+str(k)+"/")
                process.read()
            except:
                print "Error with s3 = "+str(cv)+"; k = "+str(k)
            

def optimizeAsymmetry(dataFile1,dataFile2, nprocess=2):
    # edit DETECT_THRESH for sExtractor
    k_values = [0.8, 1.0, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    output_file_a2 = "optimize/a2.csv"
    output_file_a3 = "optimize/a3.csv"
    # edit DETECT_THRESH for sExtractor
    for k in k_values:
        for line in fileinput.FileInput(sExtractorParamFile1, inplace=1):
            if not desiredParam in line:
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                    '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')
        for line in fileinput.FileInput(sExtractorParamFile2, inplace=1):
            if not desiredParam in line:
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                sys.stdout.write('DETECT_THRESH    ' + str(k) + 
                    '            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n')

        metricsA2 = []
        metricsA3 = []
        print "k = "+str(k)
        print "Nprocess = "+str(nprocess)
        parser = ConfigParser.ConfigParser()
        parser.add_section("File_Configuration")
        parser.add_section("Output_Configuration")
        parser.add_section("Indexes_Configuration")
        parser.set("File_Configuration","Indexes","A")
        parser.set("Output_Configuration","Verbose",False)
        parser.set("Output_Configuration","SaveFigure",False)
        parser.set("Indexes_Configuration","butterworth_order",2.0)
        parser.set("File_Configuration","cleanit",False)
        parser.set("File_Configuration","download",False)
        parser.set("File_Configuration","band","r") ## Paulo_25-07-17

        with open("ParallelConfig.ini","w") as cfgfile:
            parser.write(cfgfile)
        runPCymorph(fileE,nprocess)
        process = os.popen("mv output/result.csv output/r1.csv")
        out = process.read()  
        runPCymorph(fileL,nprocess)
        process = os.popen("mv output/result.csv output/r2.csv")
        process.read()
        print "Running boxCounting metric"
        try:
            nm = runMetric("output/r1.csv", "output/r2.csv", "sA2")
            nm.insert(0,k)
            metricsA2.append(nm)
            df = pd.DataFrame(metricsA2)
            df.columns = ["k","SepBCA", "SepBCL", "SepMean", "SepRoot"]
            print(df)
            df.to_csv(output_file, index=False)

        except:
            print "Error with sA2; k = "+str(k)
        try:
            nm = runMetric("output/r1.csv","output/r2.csv","sA3")
            nm.insert(0,k)
            metricsA3.append(nm)
            df = pd.DataFrame(metricsA3)
            df.columns = ["k","SepBCA", "SepBCL", "SepMean", "SepRoot"]
            print(df)
            df.to_csv(output_file, index=False)

            process = os.popen("mkdir output/A_k"+str(k))
            process.read()
            process = os.popen("mv output/r1.csv output/r2.csv output/A_k"+str(k)+"/")
            process.read()
        except:
            print "Error with sA3; k = "+str(k)

##The files must already be in Field/
if __name__ == "__main__":
    n=int(sys.argv[1])
    # early_type, late_type = sys.argv[2], sys.argv[3]
    #sm = [0.1,1.0],nsamples=18 
    optimizeSmoothness(sm = [0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8],dataFile1="test1000/1000_S_k20.csv",dataFile2="test1000/1000_E_k20.csv",nprocess=n)
    # optimizeAsymmetry(dataFile1=early_type,dataFile2=late_type,nprocess=n)
    # optimizeGa(gaTol=[0.0,0.02,0.04,0.06,0.08,0.1],gaATol=0.02,dataFile1="test1000/1000_S_k20.csv",dataFile2="test1000/1000_E_k20.csv",nprocess=n)
    # optimizeCN(dataFile1="test1000/1000_S_k20.csv",dataFile2="test1000/1000_E_k20.csv",nprocess=n)
    # optimizeEntropy(hm = [100,120,130,140,150,160,170,180,190,200,210,220,230,240,250],dataFile1="test1000/1000_S_k20.csv",dataFile2="test1000/1000_E_k20.csv",nprocess=n)
