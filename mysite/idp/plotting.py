# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 16:43:00 2014

@author: jahad
"""

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
def phasePlot(fp,fm,seqname,saveAs):
    if(os.path.exists(saveAs)):
        os.remove(saveAs)
    for x,y,label in zip(fp,fm,seqname):
        plt.scatter(x,y,marker='.',color='Black')
        plt.annotate(label,xy=(x+.01,y+.01))
    reg1, = plt.fill([0,0,.25],[0,.25,0],color = 'Chartreuse',alpha=.75)
    reg2, = plt.fill([0,0,.35,.25],[.25,.35,0,0],color = 'MediumSeaGreen',alpha=.75)
    reg3, = plt.fill([0,.35,.65,.35],[.35,.65,.35,0],color = 'DarkGreen',alpha=.75)
    reg4, = plt.fill([0,0,.35],[.35,1,.65],color = 'Red',alpha=.75)
    reg5, = plt.fill([.35,.65,1],[0,.35,0],color = 'Blue',alpha=.75)
    plt.ylim([0,1])
    plt.xlim([0,1])
    plt.xlabel('f+')
    plt.ylabel('f-')
    plt.title('Phase Diagram')
    fontP = FontProperties()
    fontP.set_size('x-small')
    plt.legend([reg1,reg2,reg3,reg4,reg5],
               ['Weak Polyampholytes & Polyelectrolytes:\nGlobules & Tadpoles',
                                           'Boundary Region',
                                           'Strong Polyampholytes:\nCoils, Hairpins, Chimeras',
                                           'Negatively Charged Strong Polyelectrolytes:\nSwollen Coils',
                                           'Positively Charged Strong Polyelectrolytes:\nSwollen Coils'],
                prop = fontP)
    plt.savefig(saveAs,dpi=200)
    plt.close()
    return plt

def testPhasePlot():
    graph = phasePlot([.65,.32,.15],[.34,.21,.42],['derp1','harro','nyan'],'C:\\Users\\James Ahad\\Documents\\GitHub\\idpserver\\mysite\\output\\test.png')


def testPhasePlotNull():
    graph = phasePlot([],[],[],'/work/jahad/IDP_patterning/idpserver/mysite/output/test.png')


import computation as comp
def NCPRPlot(sequence, bloblen, saveAs):
    if(not sequence is None):
        data = sequence.NCPRdist(bloblen)
        plt.plot(data[0,:], data[1,:])
    else:
        plt.plot([],[])
        plt.xlim([0,50])
    plt.title('NCPR Distribution')
    plt.xlabel('Blob Index')
    plt.ylabel('NCPR')
    plt.ylim([-1.1,1.1])
    plt.savefig(saveAs, dpi=200)
    plt.close()
    return plt

def testNCPRPlot():
    graph = NCPRPlot(comp.Sequence('EEEEEEKKKKEKEKEKEKEKEEEEEEEKKKKKKEKEKEKEKEKEKEKGGGGGGKEKEKE'),5, 'C:\\Users\\James Ahad\\Documents\\GitHub\\idpserver\\mysite\\output\\testNCPR.png')

def SigmaPlot(sequence, bloblen, saveAs):
    if(not sequence is None):
        data = sequence.Sigmadist(bloblen)
        plt.plot(data[0,:], data[1,:])
    else:
        plt.plot([],[])
        plt.xlim([0,50])
    plt.title('Sigma Distribution')
    plt.xlabel('Blob Index')
    plt.ylabel('Sigma')
    plt.ylim([-.1,1.1])
    plt.savefig(saveAs, dpi=200)
    plt.close()
    return plt

def testSigmaPlot():
    graph = SigmaPlot(comp.Sequence('EEEEEEKKKKEKEKEKEKEKEEEEEEEKKKKKKEKEKEKEKEKEKEKGGGGGGKEKEKE'),5, 'C:\\Users\\James Ahad\\Documents\\GitHub\\idpserver\\mysite\\output\\testSigma.png')

def HydroPlot(sequence, bloblen, saveAs):
    if(not sequence is None):
        data = sequence.Hydrodist(bloblen)
        plt.plot(data[0,:], data[1,:])
    else:
        plt.plot([],[])
        plt.xlim([0,50])
    plt.title('Hydropathy Distribution')
    plt.xlabel('Blob Index')
    plt.ylabel('Hydropathy')
    plt.savefig(saveAs, dpi=200)
    plt.close()
    return plt

def testHydroPlot():
    graph = HydroPlot(comp.Sequence('EEEEEEKKKKEKEKEKEKEKEEEEEEEKKKKKKEKEKEKEKEKEKEKGGGGGGKEKEKE'),5, 'C:\\Users\\James Ahad\\Documents\\GitHub\\idpserver\\mysite\\output\\testHydro.png')

testNCPRPlot()
testSigmaPlot()
testHydroPlot()