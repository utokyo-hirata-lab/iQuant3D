import re
import os
import os.path
import sys
import glob
import csv
import xlrd
import shutil
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from statistics import mean, median,variance,stdev
from PIL import Image
from skimage import data
from sklearn.cluster import KMeans

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

class iq3t():
    def __init__(self,folder,standard_element,washout,band_width):
        self.standard_element = standard_element
        self.washout = washout
        self.folder = os.getcwd()+'/'+folder
        self.band_width = band_width
        self.noise_cut_factor = 3

    def get_element_list(self,filepath):
        print('[ '+pycolor.YELLOW+'Processing'+pycolor.END+' ] '+filepath)
        elements = pd.read_csv(filepath,skiprows=13,header=None,dtype='str',low_memory=False)[0:1]
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

    def time_stamp(self,filepath,standard_element):
        ts = []
        elements = pd.read_csv(filepath,skiprows=13,header=None,dtype='str',low_memory=False)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        df = pd.read_csv(filepath,skiprows=15,names=names,low_memory=False)
        frag = 200
        pco_std = self.noise_cut(self.noise_cut_factor,df[standard_element])
        count,i,i_init,linenum = -1E5,0,0,0
        for t in pco_std:
            if t > frag:
                if i_init == 0:
                    i_init = i
                count = 0
            if t < frag:
                count += 1
            if count >= self.washout:
                x = df['Time'][i_init-1 :i-self.washout-1]
                y = df[standard_element][i_init-1 :i-self.washout-1]
                if len(y) > 200:
                    ts.append([x.min(),x.max()])
                    i_init = 0
                    linenum += 1
                    count = 0
            i += 1
        width,fixed_ts = [],[]
        for i in ts:
            width.append(i[1]-i[0])
        front_anchor = []
        for i in range(len(ts)-1):
            front_anchor.append(ts[i+1][0]-ts[i][0])
        peak_span = mean(front_anchor)
        t = int(ts[0][0])
        for i in ts:
            fixed_ts.append([t-2,t+int(mean(width))+2])
            t += peak_span
        return fixed_ts

    def iq3_imaging(self,filepath,standard_element,imaging_element,time_stamp):
        elements = pd.read_csv(filepath,skiprows=13,header=None,low_memory=False)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        df = pd.read_csv(filepath,skiprows=15,names=names,low_memory=False)

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
        backsignal = 1E4
        merged_line = merged_line + backsignal

        #plt.figure()
        sns.set()
        plt.style.use('dark_background')
        grid_kws = {"height_ratios": (.9, .05), "hspace": .1}
        fig, (ax, cbar_ax) = plt.subplots(2, gridspec_kw=grid_kws, figsize=(9,9))
        sns.heatmap(merged_line.T,cmap='jet',xticklabels=False,yticklabels=False,norm=LogNorm(vmin=merged_line.values.min(), vmax=merged_line.values.max()),ax=ax,cbar_ax=cbar_ax,cbar_kws={"orientation": "horizontal"})
        ax.set_title(imaging_element,color='white',fontsize=18, fontweight="bold")
        #outname = filepath.split('.')[0]+'_'+imaging_element+'_mapping.pdf'
        #print('[ '+pycolor.GREEN+'Generate'+pycolor.END+' ] '+outname)
        #plt.savefig(outname)
        #print('[ '+pycolor.BLUE+'Success'+pycolor.END+'  ] '+outname)
        outname = filepath.split('.')[0]+'_'+imaging_element+'_mapping.png'
        print('[ '+pycolor.GREEN+'Generate'+pycolor.END+'   ] '+outname)
        plt.savefig(outname)
        print('[ '+pycolor.BLUE+'Success'+pycolor.END+'    ] '+outname)
        plt.style.use('default')
        plt.close(fig)

    def iq3_imaging_rapid(self,filepath,standard_element,imaging_element,time_stamp):
        elements = pd.read_csv(filepath,skiprows=13,header=None)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        df = pd.read_csv(filepath,skiprows=15,names=names)
        #peak_analysis
        target = imaging_element
        merged_line = pd.DataFrame()
        linenum = 0
        for tsp in time_stamp:
            y = df.query('%d < Time < %f' % (tsp[0],tsp[1]))[target]
            merged_line['line'+str(linenum)] = pd.Series(list(y))
            linenum += 1

        merged_line = merged_line +1E5

        sns.set()
        plt.style.use('dark_background')
        sns.heatmap(merged_line.T,cmap='jet',xticklabels=False,yticklabels=False,norm=LogNorm(vmin=merged_line.values.min(), vmax=merged_line.values.max()),cbar=False)
        outname = filepath.split('.')[0]+'_'+imaging_element+'_mapping.png'
        print('[ '+pycolor.GREEN+'Generate'+pycolor.END+'   ] '+outname)
        plt.tight_layout()
        plt.savefig(outname,facecolor="black", edgecolor="black")
        print('[ '+pycolor.BLUE+'Success'+pycolor.END+'    ] '+outname)
        plt.close()

    def finishing(self):
        print('[ '+pycolor.YELLOW+'Moving '+pycolor.END+'    ] *.xlsx > result')
        dirname = self.folder+'/result'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*.xlsx '+self.folder+'/result')

        print('[ '+pycolor.YELLOW+'Moving '+pycolor.END+'    ] *signal.pdf > signal')
        dirname = self.folder+'/signal'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*signal.pdf '+self.folder+'/signal')

        #print('[ '+pycolor.GREEN+'Moving '+pycolor.END+'  ] *mapping.pdf > mapping')
        #dirname = os.getcwd()+'/mapping'
        #if os.path.isdir(dirname) == False:os.mkdir(dirname)
        #os.system('mv *mapping.pdf mapping')

        print('[ '+pycolor.YELLOW+'Moving '+pycolor.END+'    ] *mapping.png > mapping')
        dirname = self.folder+'/mapping'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*mapping.png '+self.folder+'/mapping')

    def clustering(self,cnumber):
        if os.path.isdir(self.folder+'/mapping_group') == True:
            os.system('rm -rf '+self.folder+'/mapping_group')
            print('[ '+pycolor.YELLOW+'Remove'+pycolor.END+'     ] data/mapping_group')

        for path in os.listdir(self.folder+'/mapping'):
            #path = path.split('.')[0]
            if os.path.isdir(self.folder+'/mapping_convert') == False:os.mkdir(self.folder+'/mapping_convert')
            #if os.path.isdir(self.folder+'/mapping_group') == False:os.mkdir(self.folder+'/mapping_group')
            img = Image.open(f'{self.folder}/mapping/{path}')
            img = img.convert('RGB')
            img_resize = img.resize((200, 200))
            path = path.split('.')[0]
            img_resize.save(f'{self.folder}/mapping_convert/{path}.jpg')
        feature = np.array([data.imread(f'{self.folder}/mapping_convert/{path}') for path in os.listdir(self.folder+'/mapping_convert')])
        feature = feature.reshape(len(feature), -1).astype(np.float64)
        model = KMeans(n_clusters=cnumber).fit(feature)
        labels = model.labels_
        for label, path in zip(labels, os.listdir(self.folder+'/mapping_convert')):
            os.makedirs(f'{self.folder}/mapping_group/{label}', exist_ok=True)
            shutil.copyfile(f"{self.folder}/mapping/{path.replace('.jpg', '.png')}", f"{self.folder}/mapping_group/{label}/{path.replace('.jpg', '.png')}")
            print('[ '+pycolor.BLUE+'Clustering'+pycolor.END+' ] '+ path + ' > ' + str(label))

    def multi_layer(self,element):
        outname = self.folder+'/'+element+'_3D.png'
        print('[ '+pycolor.GREEN+'Generate'+pycolor.END+'   ] '+outname)
        datalist = sorted(glob.glob(self.folder+'/result/*'+element+'.xlsx'))
        input_book = pd.read_excel(datalist[0], index_col=0)
        vmin = input_book.values.min()
        vmax = input_book.values.max()
        plt.figure(figsize=(6*len(datalist),6))
        for i in range(len(datalist)):
            plt.subplot(1,len(datalist),i+1)
            input_book = pd.read_excel(datalist[i], index_col=0)
            sns.set()
            plt.style.use('dark_background')
            input_book = input_book + 1E4
            sns.heatmap(input_book,cmap='jet',xticklabels=False,yticklabels=False,norm=LogNorm(vmin=vmin, vmax=vmax),cbar=False)
            print('[ '+pycolor.GREEN+'Sectioning'+pycolor.END+' ] '+datalist[i])
            plt.title(element+' (Layer='+datalist[i].split('/')[-1].split('_')[0]+')',color='white',fontsize=18, fontweight="bold")
        plt.tight_layout()
        plt.savefig(outname)
        print('[ '+pycolor.BLUE+'Success'+pycolor.END+'    ] '+outname)
        dirname = self.folder+'/multi_layer'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*.png '+self.folder+'/multi_layer')
        print('[ '+pycolor.YELLOW+'Moving '+pycolor.END+'    ] '+element+'_3D.png > multi_layer')
        plt.close()

    def finish_code(self):
        print('[ '+pycolor.YELLOW+'Shutdown'+pycolor.END+'   ] Thank you for always using iQuant3D-terminal.')

    def run(self):
        datalist = glob.glob(self.folder+'/*.csv')
        ts = self.time_stamp(datalist[0],self.standard_element)
        [[self.iq3_imaging(filepath,self.standard_element, ie, ts) for ie in self.get_element_list(filepath)] for filepath in datalist]
        self.finishing()

    def run_rapid(self):
        datalist = glob.glob(self.folder+'/*.csv')
        ts = self.time_stamp(datalist[0],self.standard_element)
        [[self.iq3_imaging_rapid(filepath,self.standard_element, ie, ts) for ie in self.get_element_list(filepath)] for filepath in datalist]
        self.finishing()

    def run_test(self):
        datalist = glob.glob(self.folder+'/*.csv')
        ts = self.time_stamp(datalist[0],self.standard_element)
        self.iq3_imaging(datalist[0],self.standard_element, self.standard_element, ts)
        dirname = self.folder+'/test_scan'
        if os.path.isdir(dirname) == False:os.mkdir(dirname)
        os.system('mv '+self.folder+'/*.xlsx '+self.folder+'/test_scan')
        os.system('mv '+self.folder+'/*signal.pdf '+self.folder+'/test_scan')
        os.system('mv '+self.folder+'/*mapping.png '+self.folder+'/test_scan')
        print('[ '+pycolor.YELLOW+'Checking'+pycolor.END+'   ] Please check /data/test_scan folder.')
