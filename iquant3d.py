import csv
import os
import sys
import re
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
from statistics import mean, median,variance,stdev
import tkinter as tk
import tkinter.messagebox, tkinter.filedialog
import glob

class pycolor:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

def vis_params():
    #plt.rcParams['axes.axisbelow'] = True
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 18
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.major.width'] = 1.0
    plt.rcParams['ytick.major.width'] = 1.0
    plt.rcParams['lines.linewidth'] = 0.8

try: from sklearn import linear_model;clf = linear_model.LinearRegression()
except ModuleNotFoundError:
    print('sklearn module was not found.')
    print('You should run '+pycolor.RED +'\"pip install sklearn\"'+pycolor.END)
    sys.exit()

try: import xlrd
except ModuleNotFoundError:
    print('xlrd module was not found.')
    print('You should run '+pycolor.RED +'\"pip install xlrd\"'+pycolor.END)
    sys.exit()

try: import openpyxl
except ModuleNotFoundError:
    print('openpyxl module was not found.')
    print('You should run '+pycolor.RED +'\"pip install openpyxl\"'+pycolor.END)
    sys.exit()

try: import xlwt
except ModuleNotFoundError:
    print('xlwt module was not found.')
    print('You should run '+pycolor.RED +'\"pip install xlwt\"'+pycolor.END)
    sys.exit()

try: import xlsxwriter
except ModuleNotFoundError:
    print('xlsxwriter module was not found.')
    print('You should run '+pycolor.RED +'\"pip install xlsxwriter\"'+pycolor.END)
    sys.exit()

try: import pprint
except ModuleNotFoundError:
    print('pprint module was not found.')
    print('You should run '+pycolor.RED +'\"pip install pprint\"'+pycolor.END)
    sys.exit()

try: import glob
except ModuleNotFoundError:
    print('glob module was not found.')
    print('You should run '+pycolor.RED +'\"pip install glob\"'+pycolor.END)
    sys.exit()

try: import pandas
except ModuleNotFoundError:
    print('pandas module was not found.')
    print('You should run '+pycolor.RED +'\"pip install pandas\"'+pycolor.END)
    sys.exit()

try: import seaborn as sns
except ModuleNotFoundError:
    print('seaborn module was not found.')
    print('You should run '+pycolor.RED +'\"pip install seaborn\"'+pycolor.END)
    sys.exit()

class iq3:
    def __init__(self):
        self.data = pd.DataFrame()

    def data_read(self,raw_csv):
        elements = pd.read_csv(raw_csv,skiprows=13,header=None)[0:1]
        names = [str(elements[i][0]).split('|')[0].replace(' ','') for i in range(len(elements.columns))]
        df = pd.read_csv('20191022_2_1.csv',skiprows=15,names=names)
        self.data = df
        print(self.data)

    def show(self,element):
        #vis_params()
        plt.plot(self.data['Time'],self.data[element],color='black')
        plt.show()
