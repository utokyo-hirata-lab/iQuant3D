import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
from matplotlib.colors import LogNorm
import os.path

class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

class iq3:
    def __init__(self,filepath,standard_element,washout,pcv):
        self.filepath = filepath
        self.standard_element = standard_element
        self.washout = washout
        self.pseudo_cutoff_value = pcv

    def get_element_list(self):
        elements = pd.read_csv(self.filepath,skiprows=13,header=None)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        return names[1:len(names)-1]

    def iq3_imaging(self,imaging_element):
        elements = pd.read_csv(self.filepath,skiprows=13,header=None)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        df = pd.read_csv(self.filepath,skiprows=15,names=names)
        frag = self.pseudo_cutoff_value

        #peak_analysis
        target = imaging_element
        merged_line = pd.DataFrame()
        fig = plt.figure(figsize=(15,3))
        ax = fig.add_subplot(111)
        plt.rcParams['lines.linewidth'] = 0.3
        pseudo_cutoff,psdf = df[self.standard_element][0:125].mean()/2,df.copy(deep=False)
        pseudo_cutoff = frag
        psdf.loc[psdf[self.standard_element] < pseudo_cutoff,self.standard_element] = 0
        #print(psdf)
        plt.plot(df['Time'],df[target],color='black',linewidth=0.3)

        #peak_wide and background
        count,i,i_init,linenum = -1E5,0,0,0
        for t in df[self.standard_element]:
            if t > frag:
                if i_init == 0:
                    i_init = i
                count = 0
            if t < frag:
                count += 1
            if count >= self.washout:
                x = df['Time'][i_init-1 :i-self.washout-1]
                y = df[target][i_init-1 :i-self.washout-1]
                #print(len(y))
                #print(len(x),linenum,len(y))
                if len(y) >= 570:
                    merged_line['line'+str(linenum)] = pd.Series(list(y))
                    ax.axvspan(x.min()+1,x.max()-1,color = "lightgray")
                    peak_wide = (i-self.washout-1) - (i_init-1)
                    background = y.mean()
                    i_init = 0
                    linenum += 1
                    count = 0
            i += 1

        outname = self.filepath.split('.')[0]+'_'+imaging_element+'_signal.pdf'
        plt.show()
