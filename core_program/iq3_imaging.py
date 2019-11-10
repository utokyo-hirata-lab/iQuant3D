
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
from matplotlib.colors import LogNorm
import os.path

#-----------------------------
filepath = '20191022_2_1.csv'
standard_element = '206Pb'
#-----------------------------

if len(sys.argv) == 2:filepath = sys.argv[1]
elif len(sys.argv) == 3:standard_element = sys.argv[2]

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
lines = 41
luster_speed = 300
washout = 20
wide_cutofff = 5

def get_element_list(filepath):
    elements = pd.read_csv(filepath,skiprows=13,header=None)[0:1]
    names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
    return names[1:len(names)-1]

def iq3_imaging(filepath,standard_element,imaging_element):
    elements = pd.read_csv(filepath,skiprows=13,header=None)[0:1]
    names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
    df = pd.read_csv('20191022_2_1.csv',skiprows=15,names=names)
    frag = 250

    #peak_analysis
    target = imaging_element
    merged_line = pd.DataFrame()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.rcParams['lines.linewidth'] = 0.3
    pseudo_cutoff,psdf = df[standard_element][50:250].mean(),df.copy(deep=False)
    psdf.loc[psdf[standard_element] < pseudo_cutoff,standard_element] = 0
    plt.plot(df['Time'],df[target],color='black',linewidth=0.3)

    #peak_wide and background
    count,i,i_init,linenum = -1E5,0,0,0
    for t in df[standard_element]:
        if t > 0:
            if i_init == 0:
                i_init = i
            count = 0
        if t == 0:
            count += 1
        if count >= washout:
            x = df['Time'][i_init-1 :i-washout-1]
            y = df[target][i_init-1 :i-washout-1]
            if len(y) >= 1:
                merged_line['line'+str(linenum)] = pd.Series(list(y))
                ax.axvspan(x.min()+1,x.max()-1,color = "lightgray")
                peak_wide = (i-washout-1) - (i_init-1)
                background = y.mean()
                i_init = 0
                linenum += 1
                count = 0
        i += 1

    outname = filepath.split('.')[0]+'_'+imaging_element+'_signal.pdf'
    print('[ '+pycolor.GREEN+'Generate'+pycolor.END+' ] '+outname)
    plt.savefig(outname)
    print('[ '+pycolor.BLUE+'Success'+pycolor.END+'  ] '+outname)
    plt.close()

    plt.figure()
    merged_line = merged_line+1E5
    outname = filepath.split('.')[0]+'_'+imaging_element+'.xlsx'
    print('[ '+pycolor.GREEN+'Generate'+pycolor.END+' ] '+outname)
    merged_line.T.to_excel(outname, sheet_name=imaging_element)
    print('[ '+pycolor.BLUE+'Success'+pycolor.END+'  ] '+outname)
    sns.heatmap(merged_line.T,cmap='jet',norm=LogNorm(vmin=merged_line.values.min(), vmax=merged_line.values.max()),cbar=None)
    outname = filepath.split('.')[0]+'_'+imaging_element+'_mapping.pdf'
    print('[ '+pycolor.GREEN+'Generate'+pycolor.END+' ] '+outname)
    plt.savefig(outname)
    print('[ '+pycolor.BLUE+'Success'+pycolor.END+'  ] '+outname)
    plt.close()

def finishing(filepath):
    print('[ '+pycolor.GREEN+'Moving '+pycolor.END+'  ] *mapping.pdf > mapping')
    dirname = os.getcwd()+'/mapping'
    if os.path.isdir(dirname) == False:os.mkdir(dirname)
    os.system('mv *mapping.pdf mapping')

    print('[ '+pycolor.GREEN+'Moving '+pycolor.END+'  ] *.xlsx > result')
    dirname = os.getcwd()+'/result'
    if os.path.isdir(dirname) == False:os.mkdir(dirname)
    os.system('mv *.xlsx result')

    print('[ '+pycolor.GREEN+'Moving '+pycolor.END+'  ] *signal.pdf > signal')
    dirname = os.getcwd()+'/signal'
    if os.path.isdir(dirname) == False:os.mkdir(dirname)
    os.system('mv *signal.pdf signal')

[iq3_imaging(filepath,standard_element, ie) for ie in get_element_list(filepath)]
finishing(filepath)
