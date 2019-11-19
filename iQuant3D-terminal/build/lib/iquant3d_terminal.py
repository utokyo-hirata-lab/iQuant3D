
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
from matplotlib.colors import LogNorm
import os.path
import glob

#-----------------------------
filepath = '20191110_3dimaging_001_1.csv'
standard_element = '206Pb'
washout = 20
#----------------------------

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

#user_input

class iq3t():
    def __init__(self,folder,standard_element,washout):
        self.standard_element = standard_element
        self.washout = washout
        self.folder = folder

    def get_element_list(self,filepath):
        print('[ '+pycolor.YELLOW+'Processing'+pycolor.END+' ] '+filepath)
        elements = pd.read_csv(filepath,skiprows=13,header=None,dtype = 'str')[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        return names[1:len(names)-1]

    def noise_cut(self,n,data):
        y = []
        for i in range(n):y.append(0)
        for i in range(n,len(data)-n):
            if data[i-n]-data[i+n] == 0:y.append(0)
            else:y.append(data[i])
        for i in range(n):y.append(0)
        return y

    def time_stamp(self, n, filepath,standard_element):
        ts = []
        elements = pd.read_csv(filepath,skiprows=13,header=None)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        df = pd.read_csv(filepath,skiprows=15,names=names)
        frag = 2000
        pco_std = self.noise_cut(n,df[standard_element])
        count,i,i_init,linenum = -1E5,0,0,0
        for t in pco_std:
            if t > frag:
                if i_init == 0:
                    i_init = i
                count = 0
            if t < frag:
                count += 1
            if count >= washout:
                x = df['Time'][i_init-1 :i-washout-1]
                y = df[standard_element][i_init-1 :i-washout-1]
                if len(y) > 570:
                    ts.append([x.min(),x.max()])
                    i_init = 0
                    linenum += 1
                    count = 0
            i += 1
        return ts

    def iq3_imaging(self,filepath,standard_element,imaging_element,time_stamp):
        elements = pd.read_csv(filepath,skiprows=13,header=None)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        df = pd.read_csv(filepath,skiprows=15,names=names)

        #peak_analysis
        target = imaging_element
        merged_line = pd.DataFrame()
        fig = plt.figure(figsize=(15,3))
        ax = fig.add_subplot(111)
        plt.rcParams['lines.linewidth'] = 0.3
        plt.plot(df['Time'],df[target],color='black',linewidth=0.3)

        linenum = 0
        for tsp in time_stamp:
            y = df.query('%d < Time < %f' % (tsp[0],tsp[1]))[target]
            merged_line['line'+str(linenum)] = pd.Series(list(y))
            ax.axvspan(tsp[0],tsp[1],color = "lightgray")
            linenum += 1

        #plt.show()
        outname = filepath.split('.')[0]+'_'+imaging_element+'_signal.pdf'
        print('[ '+pycolor.GREEN+'Generate'+pycolor.END+'   ] '+outname)
        plt.savefig(outname)
        print('[ '+pycolor.BLUE+'Success'+pycolor.END+'    ] '+outname)
        plt.close()

        outname = filepath.split('.')[0]+'_'+imaging_element+'.xlsx'
        print('[ '+pycolor.GREEN+'Generate'+pycolor.END+'   ] '+outname)
        merged_line.T.to_excel(outname, sheet_name=imaging_element)
        print('[ '+pycolor.BLUE+'Success'+pycolor.END+'    ] '+outname)
        merged_line = merged_line+1E5

        plt.figure()
        sns.heatmap(merged_line.T,cmap='jet',norm=LogNorm(vmin=merged_line.values.min(), vmax=merged_line.values.max()),cbar=None)
        plt.title(imaging_element)
        #outname = filepath.split('.')[0]+'_'+imaging_element+'_mapping.pdf'
        #print('[ '+pycolor.GREEN+'Generate'+pycolor.END+' ] '+outname)
        #plt.savefig(outname)
        #print('[ '+pycolor.BLUE+'Success'+pycolor.END+'  ] '+outname)
        outname = filepath.split('.')[0]+'_'+imaging_element+'_mapping.png'
        print('[ '+pycolor.GREEN+'Generate'+pycolor.END+'   ] '+outname)
        plt.savefig(outname)
        print('[ '+pycolor.BLUE+'Success'+pycolor.END+'    ] '+outname)
        plt.close()

    def finishing(self):
        print('[ '+pycolor.YELLOW+'Moving '+pycolor.END+'    ] *.xlsx > result')
        dirname = os.getcwd()+'/'+self.folder+'/result'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*.xlsx '+self.folder+'/result')

        print('[ '+pycolor.YELLOW+'Moving '+pycolor.END+'    ] *signal.pdf > signal')
        dirname = os.getcwd()+'/'+self.folder+'/signal'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*signal.pdf '+self.folder+'/signal')

        #print('[ '+pycolor.GREEN+'Moving '+pycolor.END+'  ] *mapping.pdf > mapping')
        #dirname = os.getcwd()+'/mapping'
        #if os.path.isdir(dirname) == False:os.mkdir(dirname)
        #os.system('mv *mapping.pdf mapping')

        print('[ '+pycolor.YELLOW+'Moving '+pycolor.END+'    ] *mapping.png > mapping')
        dirname = os.getcwd()+'/'+self.folder+'/mapping'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*mapping.png '+self.folder+'/mapping')

    def run(self):
        datalist = glob.glob(os.getcwd()+'/'+self.folder+'/*.csv')
        [[self.iq3_imaging(filepath,self.standard_element, ie, self.time_stamp(3,datalist[0],self.standard_element)) for ie in self.get_element_list(filepath)] for filepath in datalist]
        self.finishing()
