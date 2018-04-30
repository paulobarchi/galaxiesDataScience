import scipy.stats as stats
from scipy.ndimage.filters import convolve
from scipy.ndimage.filters import median_filter
import numpy
import gridAlg
import ellipse
import indexes
import galaxyIO
import sys
import os

cimport numpy
from libc.math cimport sqrt, pow

verbose = 1

def printIfVerbose(string):
    if (verbose > 0):
        print(string)

cdef class EtaFunction:

        def _runMaskMaker(self,char* path,char* fileName,char* xtraID,float ra, float dec,float petroRad,float rowc,float colc):
        cuttedFile = str(xtraID)+'.fit'

        configFile = ConfigParser.ConfigParser()
        configFile.read('cfg/paths.ini')
        pythonPath = configFile.get("Path","Python")

        #Change directory, execute maskMaker and get back
        localPath = os.getcwd()
        newPath = os.getcwd()+'/maskMaker'
        os.chdir(newPath)
        print("maskmaker")
        cmd = pythonPath+" -W\"ignore\" maskmaker_wcut.py ../"+path+fileName+" "+str(xtraID)+" "+str(ra)+" "+str(dec)+" "+str(self.stampSize)+\
            " "+str(petroRad)+" "+str(rowc)+" "+str(colc)+" >> logMaskMaker.txt"
        pr = os.popen(cmd)
        pr.read()
        os.chdir(localPath)
        with open(str(xtraID)+"_log.txt",'r') as eF:
            self.errorVar = int(eF.read())
        os.remove(str(xtraID)+"_log.txt")
        return cuttedFile

    #@profile
    def run(self,char *fpath,char * image,mask_File='',char *saveResult="",float petroRad=0.0,float rowc=0.0,float colc=0.0,float ra=-1.0,float dec=-1.0,calibratedData=False,char* xtraID='', saveFig=True, clear=False,clip=False):
        cdef:
                #image proprieties 
                int width, heigth, it

                #matrices
                float[:,:] notMasked, mask, segmentation, scaleMatrix, segmentationMask, removedGalaxies, zeros
                float[:,:] matInverse, matSmoth, matSmoothness, transformed, transformedEll, transformed2, transformedEll2

                #indexes:
                float a2, a3, s2, s3,h, sp2, sp3, ga, c1, c2
                float sa2, sa3, ss2, ss3,sh, ssp2, ssp3
                float oa2, oa3, os2, os3,oh, osp2, osp3


        results = [xtraID]
        labels = ["Id"]
        printIfVerbose("Running File: "+fpath+image)
        maskFile = mask_File
        fileName = image
        path= fpath
        if (ra != -1.0) and (dec != -1.0) and (clip==True):
            fileName = self._runMaskMaker(path, image,xtraID,ra,dec,petroRad,rowc,colc)
            path = 'cutted/'
         
        printIfVerbose("Reading File: "+path+fileName)
        notMasked = galaxyIO.readFITSIMG(path+fileName)
        heigth, width = len(notMasked), len(notMasked[0])
        galaxyIO.runSextractor(path,fileName,xtraID)

        if (maskFile == ''):
            printIfVerbose("No mask... Considering every point in the image")
            mask = numpy.array([[0.0 for j in range(width)] for i in range(heigth)],dtype=numpy.float32)
        else:
            printIfVerbose("Reading mask file "+path+maskFile)
            mask = galaxyIO.readFITSIMG(path+maskFile)
        # primeira rodada do sextractor (com a imagem contaminada)
        printIfVerbose("Running Sextractor")
        segmentation = galaxyIO.readFITSIMG(str(xtraID)+"_seg.fits")
        bcg = galaxyIO.readFITSIMG(str(xtraID)+"_bcg.fits")
        dic, data = galaxyIO.readSextractorOutput(str(xtraID)+".cat")
        dicFiltered, dataFiltered = galaxyIO.filterSextractorData(mask, dic, data)
        if clear:
            self.clearIt(fileName,xtraID)
        printIfVerbose("Interpolating ellipse")
        e = ellipse.ellipse(dic,dataFiltered,calibratedData,self.sky)
        segmentationMask, idGalaxy, segMax = gridAlg.filterSegmentedMask(segmentation,e)
        removedGalaxies = gridAlg.removeOtherGalaxies(notMasked, segmentation, idGalaxy)
        newMat, holes = gridAlg.interpolateEllipse(removedGalaxies,e)

        galaxyIO.plotFITS(newMat,"cutted/"+str(xtraID)+".fit")
        printIfVerbose("Running Sextractor again")

        #segunda rodada do sextractor (com a imagem limpa)
        #calibrando pelo background
        converged = False
        bcgW = 32
        galaxyIO.runSextractor("cutted/", str(xtraID)+".fit", xtraID,["BACK_SIZE"],[bcgW])
        segmentation = galaxyIO.readFITSIMG(str(xtraID)+"_seg.fits")
        bcg = galaxyIO.readFITSIMG(str(xtraID)+"_bcg.fits")
        dic, data = galaxyIO.readSextractorOutput(str(xtraID)+".cat")
        dicFiltered, dataFiltered = galaxyIO.filterSextractorData(mask, dic, data)
        if clear:
            self.clearIt(fileName,xtraID)
        if saveFig:
            galaxyIO.plotFITS(bcg,"imgs/bcg"+str(bcgW)+".fit")
        printIfVerbose("Calculating flux profile")
        # try:
        Concentration_Density = 100
        calcEtaFunction(newMat, bcg, e, Concentration_Density);
