# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 11:24:43 2014

@author: James Ahad
"""

import csv
import numpy as np

class Residue:
    def __init__(self,name,letterCode3,letterCode1,hydropathy,charge):
        self.name = name
        self.letterCode3 = letterCode3
        self.letterCode1 = letterCode1
        self.hydropathy = hydropathy
        self.charge = charge

class resTable:
    def __init__(self,filename):
        self.filename = filename
        self.resTab = []
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                res = Residue(row[0],row[1],row[2],float(row[3]),int(row[4]))
                self.resTab = np.append(self.resTab,res)

    def lookForRes(self,resCode,codeType=1):
        if(codeType == 1):
            return next((x for x in self.resTab if x.letterCode1 == resCode), None)
        elif(codeType == 3):
            return next((x for x in self.resTab if x.letterCode3 == resCode), None)
        else:
            return None

    def lookUpHydropathy(self,resCode,codeType=1):
        res = self.lookForRes(resCode,codeType)
        if(res == None):
            print('Illegal residue code or codeType\nLegal code types are 1 and 3\nResidue codes must be the corresponding 1 letter or 3 letter code for a given residue\n')
            return 0
        return self.lookForRes(resCode,codeType).hydropathy

    def lookUpCharge(self,resCode,codeType=1):
        #first check for reduced residue types (aka charge +/-/0)
        if(resCode == '+'):
            return 1
        elif(resCode == '-'):
            return -1
        elif(resCode == '0'):
            return 0
        else:
            res = self.lookForRes(resCode,codeType)
            if(res == None):
                print('Illegal residue code or codeType\nLegal code types are 1 and 3\nResidue codes must be the corresponding 1 letter or 3 letter code for a given residue\n')
                return 0
            return self.lookForRes(resCode,codeType).charge

    def one2three(self, resCode):
        return self.lookForRes(resCode, 1).letterCode3

    def three2one(self, resCode):
        return self.lookForRes(resCode, 3).letterCode1


# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:10:55 2014

@author: jahad
"""

import random as rng
import time as t
import copy as cp
import os
base = os.path.dirname(__file__)
resData = os.path.join(os.path.join(base, os.pardir),'residueData.csv')
lkupTab = resTable(resData)

class Sequence:
    def __init__(self,seq,dmax = -1,chargePattern=[]):
        self.seq = seq.upper()
        self.len = len(seq)
        self.chargePattern = chargePattern
        if(chargePattern == []):
            for i in np.arange(0,self.len):
                if(lkupTab.lookUpCharge(self.seq[i])>0):
                    chargePattern = np.append(chargePattern,1)
                elif(lkupTab.lookUpCharge(self.seq[i])<0):
                    chargePattern = np.append(chargePattern,-1)
                else:
                    chargePattern = np.append(chargePattern,0)
            self.chargePattern = chargePattern
        self.dmax = dmax #initializing to prevent extra computational time
        self.N_ITERS = 5
        self.N_STEPS = 5000

    def countPos(self):
        return len(np.where(self.chargePattern>0)[0])

    def countNeg(self):
        return len(np.where(self.chargePattern<0)[0])

    def countNeut(self):
        return len(np.where(self.chargePattern==0)[0])

    def Fplus(self):
        return self.countPos()/(self.len+0.0)

    def Fminus(self):
        return self.countNeg()/(self.len+0.0)

    def FCR(self):
        return (self.countPos() + self.countNeg())/(self.len+0.0)

    def NCPR(self):
        return (self.countPos() - self.countNeg())/(self.len+0.0)

    def phasePlotRegion(self):
        fcr = self.FCR()
        ncpr = self.NCPR()
        if(fcr < .25 and ncpr<.25):
            return 1
        elif(fcr >= .25 and fcr <= .35 and ncpr <= .35):
            return 2
        elif(fcr > .35 and ncpr <= .35):
            return 3
        elif(fcr > .35 and ncpr > .35):
            if(self.Fplus>.35):
                return 4
            elif(self.Fminus>.35):
                return 5
            else: #This case is impossible but here for completeness
                return None
        else: #This case is impossible but here for completeness
            return None


    def phasePlotAnnotation(self):
        region = self.phasePlotRegion()
        if(region == 1):
            return 'Globule/Tadpole'
        elif(region == 2):
            return 'Boundary Region'
        elif(region == 3):
            return 'Coils,Hairpins and Chimeras'
        elif(region == 4):
            return 'Negatively Charged Swollen Coils'
        elif(region == 5):
            return 'Positively Charged Swollen Coils'
        else :
            return 'ERROR, NOT A REAL REGION'

    def meanHydropathy(self):
        ans = 0
        for i in np.arange(0,self.len):
            ans += lkupTab.lookUpHydropathy(self.seq[i])/self.len
        return ans

    def cumMeanHydropathy(self):
        ans = [lkupTab.lookUpHydropathy(self.seq[0])]
        for i in np.arange(1,self.len):
            ans.append(ans[i-1]+lkupTab.lookUpHydropathy(self.seq[i]))
        ans /= (np.arange(0,self.len)+1)
        return ans

    def sigma(self):
        if(self.countNeut() == self.len):
            return 0
        else:
            return self.NCPR()**2/self.FCR()

    def deltaForm(self,bloblen):
        sigma = self.sigma()
        nblobs = self.len-bloblen+1
        ans = 0
        for i in np.arange(0,nblobs):
            blob = self.chargePattern[i:(i+bloblen)]
            bpos = len(np.where(blob>0)[0])
            bneg = len(np.where(blob<0)[0])
            bncpr = (bpos-bneg)/(bloblen+0.0)
            bfcr = (bpos+bneg)/(bloblen+0.0)
            if(bfcr == 0):
                bsig = 0
            else:
                bsig = bncpr**2/bfcr
            ans += (sigma - bsig)**2/nblobs
        return ans

    def delta(self):
        return (self.deltaForm(5)+self.deltaForm(6))/2

    def deltaMax(self):
        #if this has been computed already, then return it
        if(self.dmax != -1):
            return self.dmax
        elif(self.FCR() == 0):
            self.dmax = 0
        #first computational trick (Maximum Charge Separation)
        elif(self.countNeut() == 0):
            setupSequence = ''
            for i in np.arange(0,self.countPos()):
                setupSequence += '+'
            for i in np.arange(0,self.countNeg()):
                setupSequence += '-'
            assert(self.len == len(setupSequence))
            self.dmax = Sequence(setupSequence).delta()
        #second computational trick (Maximization of # of Charged Blobs)
        elif(self.countNeut() >= 18):
            #DEBUG
            #maxSeq = ''
            nneuts = self.countNeut()
            posBlock = ''
            negBlock = ''
            for i in np.arange(0,self.countPos()):
                posBlock += '+'
            for i in np.arange(0,self.countNeg()):
                negBlock += '-'
            for startNeuts in np.arange(0,7):
                for endNeuts in np.arange(0,7):
                    setupSequence = ''
                    midBlock = ''
                    endBlock = ''
                    for i in np.arange(startNeuts):
                        setupSequence += '0'
                    for i in np.arange(0,endNeuts):
                        endBlock += '0'
                    for i in np.arange(0,nneuts-startNeuts-endNeuts):
                        midBlock += '0'
                    setupSequence += posBlock
                    setupSequence += midBlock
                    setupSequence += negBlock
                    setupSequence += endBlock
                    #DEBUG
                    #print(setupSequence)
                    #assert(len(setupSequence) == self.len)
                    nseq = Sequence(setupSequence)
                    if(nseq.delta()>self.dmax):
                        self.dmax = nseq.delta()
                        #DEBUG
                        #maxSeq = nseq.seq
        #third computational trick (Search through set of sequences that fit DMAX pattern)
        else:
            #DEBUG
            #maxSeq = ''
            posBlock = ''
            negBlock = ''
            nneuts = self.countNeut()
            for i in np.arange(0,self.countPos()):
                posBlock += '+'
            for i in np.arange(0,self.countNeg()):
                negBlock += '-'
            for midNeuts in np.arange(0,nneuts+1):
                midBlock = ''
                for i in np.arange(0,midNeuts):
                    midBlock += '0'
                for startNeuts in np.arange(0,nneuts-midNeuts+1):
                    setupSequence = ''
                    for i in np.arange(0,startNeuts):
                        setupSequence += '0'
                    setupSequence += posBlock
                    setupSequence += midBlock
                    setupSequence += negBlock
                    for i in np.arange(0,nneuts-startNeuts-midNeuts):
                        setupSequence += '0'
                    #DEBUG
                    #print(setupSequence)
                    #assert(len(setupSequence) == self.len)
                    nseq = Sequence(setupSequence)
                    if(nseq.delta()>self.dmax):
                        self.dmax = nseq.delta()
                        #DEBUG
                        #maxSeq = nseq.seq
            #DEBUG
            #print('\n' + maxSeq)
        return self.dmax

    def kappa(self):
        if(self.deltaMax() == 0):
            return 1
        return self.delta()/self.deltaMax()

    def swapRes(self,index1,index2):
        if(index1 == index2):
            return Sequence(self.seq)
        elif(index2<index1):
            temp = index2
            index2 = index1
            index1 = temp
        else:
            pass
        tempseq = self.seq[:index1] + self.seq[index2] + self.seq[(index1+1):(index2)]+ self.seq[index1] + self.seq[(index2+1):]
        charge1 = self.chargePattern[index1]
        charge2 = self.chargePattern[index2]
        tempChargeSeq = cp.deepcopy(self.chargePattern)
        tempChargeSeq[index1] = charge2
        tempChargeSeq[index2] = charge1
        for i in range(0,len(tempseq)):
            assert(lkupTab.lookUpCharge(tempseq[i]) == tempChargeSeq[i])
        return Sequence(tempseq,self.dmax,tempChargeSeq)

    def swapRandChargeRes(self):
        rand = rng.Random()
        rand.seed(t.time())
        posInd = np.where(self.chargePattern>0)[0]
        negInd = np.where(self.chargePattern<0)[0]
        neutInd = np.where(self.chargePattern==0)[0]
        if(len(neutInd) == 0):
            if(len(posInd) == 0 or len(negInd) == 0):
                print('swap will not change kappa, only one charge type in sequence')
                return self
            else:
                chargeType = [1,2]
        elif(len(negInd) == 0):
            if(len(posInd) == 0 or len(neutInd) == 0):
                print('swap will not change kappa, only one charge type in sequence')
                return self
            else:
                chargeType = [1,3]
        elif(len(posInd) == 0):
            if(len(negInd) == 0 or len(neutInd) == 0):
                print('swap will not change kappa, only one charge type in sequence')
                return self
            else:
                chargeType = [2,3]
        else:
            chargeType = rand.sample([1,2,3],2)

        if(chargeType[0] == 1):
            swapPair1 = rand.sample(posInd,1)
        elif(chargeType[0] == 2):
            swapPair1 = rand.sample(negInd,1)
        elif(chargeType[0] == 3):
            swapPair1 = rand.sample(neutInd,1)

        if(chargeType[1] == 1):
            swapPair2 = rand.sample(posInd,1)
        elif(chargeType[1] == 2):
            swapPair2 = rand.sample(negInd,1)
        elif(chargeType[1] == 3):
            swapPair2 = rand.sample(neutInd,1)
        return self.swapRes(swapPair1[0],swapPair2[0])

    def toString(self):
        s = "%i\t%3.5f\t%3.5f\t%3.5f\t%3.5f\t%3.5f\t%3.5f\t%3.5f\t%3.5f\t%3.5f" % (self.len,self.Fminus(),self.Fplus(),self.FCR(),self.NCPR(),self.sigma(),self.delta(),self.deltaMax(),self.kappa(),self.meanHydropathy())
        return s

    def toFileString(self):
        s = "Sequence: %s\n" % (self.seq)
        s += "N:\t%i\n" % (self.len)
        s += "f-:\t%3.5f\n" % (self.Fminus())
        s += "f+:\t%3.5f\n" % (self.Fplus())
        s += "FCR:\t%3.5f\n" % (self.FCR())
        s += "NCPR:\t%3.5f\n" % (self.NCPR())
        s += "Sigma:\t%3.5f\n" % (self.sigma())
        s += "Delta:\t%3.5f\n" % (self.delta())
        s += "Max Delta:\t%3.5f\n" % (self.deltaMax())
        s += "Kappa:\t%3.5f\n" % (self.kappa())
        s += "<H>:\t%3.5f\n" % (self.meanHydropathy())
        s += "Phase Plot Region: %i\n" % (self.phasePlotRegion())
        s += "Phase Plot Annotation: %s\n" % (self.phasePlotAnnotation())
        return s

    def makeCampariSeqFile(self,path):
        with open(path, 'w') as f:
            f.write('ACE\n')
            for res in self.seq:
                f.write(lkupTab.one2three(res))
                f.write('\n')
            f.write('NME\n')
            for i in range(self.countPos()):
                f.write('CL-\n')
            for i in range(self.countNeg()):
                f.write('NA+\n')
            f.write('END\n')
            f.close()
            
    def returnColoredIndexing(self):
        colors = []
        for charge in self.chargePattern:
            if(charge == 1):
                colors.append('blue')
            elif(charge == -1):
                colors.append('red')
            else:
                colors.append('black')
        return colors
        
    def returnHtmlColoredString(self):
        coloredIndexing = self.returnColoredIndexing()
        string = ''
        count = 0
        for c,s in zip(coloredIndexing,self.seq):
            count = count + 1
            if(np.mod(count,50) == 0):
                string = '%s%s' %(string,'<br>')
            string = '%s<span style="color:%s">%s</span>' % (string,c,s)
        return string
        
    def returnHtmlString(self):
        string = ''
        count = 0
        for s in self.seq:
            count = count + 1
            if(np.mod(count,50) == 0):
                string = '%s%s' %(string,'<br>')
            string = '%s<span style="color:black">%s</span>' % (string,s)
        return string