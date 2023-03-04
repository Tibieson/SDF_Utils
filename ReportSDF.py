import pandas as pd
import numpy as np
from sdf import SdfReader
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import math
from pathlib import Path
import os
import shutil
import matplotlib.colors as colors


from fpdf import FPDF
import logging
from alive_progress import alive_bar

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s [%(filename)s] [%(levelname)s] - %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)



color  = ['b', 'tab:orange', 'r', 'c','m','g','y', 'k','tab:pink','tab:olive','tab:cyan','tab:purple','tab:brown','tab:blue','tab:gray', 'tab:green', 'tab:orange','tab:red']
MARKSIZE = 2

   
def selection_criteria(file):

    file_name = file[0:11]
    measurment= file[12:16]
    timestamp = file[28:34]

    Trk_dict = {}

    if file_name == 'TC_Gen7_029':
        if timestamp == '121319' or timestamp =='133135' or timestamp =='140241':
            TC_Gen7_029 ={'NumPoints': 50, 'Latdistance_min': -4, 'Latdistance_max': 4, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 70, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_029
        elif timestamp =='132713':
            TC_Gen7_029 ={'NumPoints': 60, 'Latdistance_min': -4, 'Latdistance_max': 4, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 70, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_029
        elif timestamp =='140358':
            TC_Gen7_029 ={'NumPoints': 10, 'Latdistance_min': -4, 'Latdistance_max': 2,'SpeedOverGround_min':4, 'SpeedOverGround_max': 20,'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_029
        elif timestamp == '140103':
            TC_Gen7_029 ={'NumPoints': 10, 'Latdistance_min': -4, 'Latdistance_max': 2, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 70, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_029
        elif timestamp == '112335':
            TC_Gen7_029 ={'NumPoints': 4, 'Latdistance_min': -2.5, 'Latdistance_max': 2, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 70, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_029
        else:
            TC_Gen7_029 ={'NumPoints': 10, 'Latdistance_min': -4, 'Latdistance_max': 4, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 70, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_029

    elif file_name == 'TC_Gen7_030':
        if timestamp == '133424':
            TC_Gen7_030 ={'NumPoints': 40, 'Latdistance_min': -3, 'Latdistance_max': 3, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_030
        else:
            TC_Gen7_030 ={'NumPoints': 40, 'Latdistance_min': -6, 'Latdistance_max': 6, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_030

    elif file_name == 'TC_Gen7_031':
        if timestamp == '091544':
            TC_Gen7_031 ={'NumPoints': 50, 'Latdistance_min': -5, 'Latdistance_max': 2,'SpeedOverGround_min':6, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_031
        elif timestamp == '092548' or timestamp =='092804':
            TC_Gen7_031 ={'NumPoints': 100, 'Latdistance_min': -4, 'Latdistance_max': 2,'SpeedOverGround_min':6, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_031
        elif timestamp == '093719' or timestamp == '094554':
            TC_Gen7_031 ={'NumPoints': 0, 'Latdistance_min': -2, 'Latdistance_max': 2,'SpeedOverGround_min':4.7, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 40}
            Trk_dict= TC_Gen7_031
        elif timestamp == '093818':
            TC_Gen7_031 ={'NumPoints': 0, 'Latdistance_min': -2, 'Latdistance_max': 2, 'SpeedOverGround_min':1, 'SpeedOverGround_max': 100, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_031
        elif timestamp == '093611':
            TC_Gen7_031 ={'NumPoints': 4, 'Latdistance_min': -2.5, 'Latdistance_max': 5,'SpeedOverGround_min':2, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            #TC_Gen7_031 ={'NumPoints': 40, 'Latdistance_min': -2, 'Latdistance_max': 10,'SpeedOverGround_min':6, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 20}
            Trk_dict= TC_Gen7_031
        elif timestamp == '095057':
            TC_Gen7_031 ={'NumPoints': 30, 'Latdistance_min': -10, 'Latdistance_max': 3,'SpeedOverGround_min':6, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_031
        elif timestamp == '094003':
            TC_Gen7_031 ={'NumPoints': 10, 'Latdistance_min': -2, 'Latdistance_max': -1,'SpeedOverGround_min':6, 'SpeedOverGround_max': 10, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_031
        elif timestamp == '122134':
            TC_Gen7_031 ={'NumPoints': 10, 'Latdistance_min': -4, 'Latdistance_max': 4,'SpeedOverGround_min':3, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_031

        else:
            TC_Gen7_031 ={'NumPoints': 30, 'Latdistance_min': -10, 'Latdistance_max': 10,'SpeedOverGround_min':6, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_031

    elif file_name == 'TC_Gen7_032':
        
        if timestamp == '100816' or timestamp =='101011' or timestamp =='095603' or timestamp =='095821' or timestamp =='095603':
            TC_Gen7_032 ={'NumPoints': 50, 'Latdistance_min': -2, 'Latdistance_max': 2,'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_032
        elif timestamp == '101336' or timestamp =='101545' :
            TC_Gen7_032 ={'NumPoints': 0, 'Latdistance_min': -2, 'Latdistance_max': 2,'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_032
        elif timestamp == '122747':
            TC_Gen7_032 ={'NumPoints': 50, 'Latdistance_min': -15, 'Latdistance_max': 15,'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_032
        elif timestamp == '101807':
            TC_Gen7_032 ={'NumPoints': 4, 'Latdistance_min': -2, 'Latdistance_max': 2,'SpeedOverGround_min':5, 'SpeedOverGround_max': 7.5, 'Longdistance_min':-200, 'Longdistance_max': 2}
            Trk_dict= TC_Gen7_032
        else:
            TC_Gen7_032 ={'NumPoints': 4, 'Latdistance_min': -2, 'Latdistance_max': 2,'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_032
    
    elif file_name == 'TC_Gen7_033':
        if timestamp == '103306':
            TC_Gen7_033 ={'NumPoints': 100, 'Latdistance_min': -4, 'Latdistance_max': 6,'SpeedOverGround_min':10, 'SpeedOverGround_max': 15, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_033
        elif timestamp == '103602':
            TC_Gen7_033 ={'NumPoints': 200, 'Latdistance_min': -4, 'Latdistance_max': 6,'SpeedOverGround_min':10, 'SpeedOverGround_max': 15, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_033
        elif timestamp == '103818':
            TC_Gen7_033 ={'NumPoints': 60, 'Latdistance_min': -4, 'Latdistance_max': 4,'SpeedOverGround_min':10, 'SpeedOverGround_max': 15, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_033
        elif timestamp == '103943':
            TC_Gen7_033 ={'NumPoints': 10, 'Latdistance_min': -6, 'Latdistance_max': 6,'SpeedOverGround_min':-1, 'SpeedOverGround_max': 200, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_033
        else:
            TC_Gen7_033 ={'NumPoints': 10, 'Latdistance_min': -6, 'Latdistance_max': 6,'SpeedOverGround_min':5, 'SpeedOverGround_max': 15, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_033

    elif file_name == 'TC_Gen7_034':
        if timestamp == '115234':
            TC_Gen7_034 ={'NumPoints': 30, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 12, 'Longdistance_min':-9, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_034
        elif timestamp =='120112' :
            TC_Gen7_034 ={'NumPoints': 30, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 10, 'SpeedOverGround_max': 20,'Longdistance_min':-8, 'Longdistance_max': 30}
            Trk_dict= TC_Gen7_034
        elif timestamp =='120223':
            TC_Gen7_034 ={'NumPoints': 30, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 10, 'SpeedOverGround_max': 20,'Longdistance_min':-6.5, 'Longdistance_max': 30}
            Trk_dict= TC_Gen7_034
        elif timestamp =='114308':
            TC_Gen7_034 ={'NumPoints': 10, 'Latdistance_min': -200, 'Latdistance_max': 200, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 20,'Longdistance_min':-8, 'Longdistance_max': 2}
            Trk_dict= TC_Gen7_034
        elif timestamp =='120339':
            TC_Gen7_034 ={'NumPoints': 100, 'Latdistance_min': -200, 'Latdistance_max': 200, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 20, 'Longdistance_min':-9, 'Longdistance_max': -2.5}
            Trk_dict= TC_Gen7_034
        elif timestamp =='114530':
            TC_Gen7_034 ={'NumPoints': 10, 'Latdistance_min': -200, 'Latdistance_max': 200, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 15, 'Longdistance_min':-8, 'Longdistance_max': 0} 
            Trk_dict= TC_Gen7_034
        elif timestamp =='114750':
            TC_Gen7_034 ={'NumPoints': 400, 'Latdistance_min': -200, 'Latdistance_max': 200, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 7, 'Longdistance_min':-8, 'Longdistance_max': 5} 
            Trk_dict= TC_Gen7_034
        else:
            TC_Gen7_034 ={'NumPoints': 10, 'Latdistance_min': -200, 'Latdistance_max': 200, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 15,'Longdistance_min':-20, 'Longdistance_max': 5} 
            Trk_dict= TC_Gen7_034

    elif file_name == 'TC_Gen7_035':
        TC_Gen7_035 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 9, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}# 'TargtSpeed_min': 9, 'TargtSpeed_max': 11
        Trk_dict= TC_Gen7_035
        if timestamp == '120943' or timestamp =='121122' or timestamp =='121254':
            TC_Gen7_035 ={'NumPoints': 200, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 9, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}# 'TargtSpeed_min': 9, 'TargtSpeed_max': 11
            Trk_dict= TC_Gen7_035

    elif file_name == 'TC_Gen7_036':
        if timestamp == '122130':
            TC_Gen7_036 ={'NumPoints': 60, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 20, 'Longdistance_min':5, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_036
        elif timestamp =='122400' or timestamp == '122510':
            TC_Gen7_036 ={'NumPoints': 50, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 20, 'Longdistance_min':5, 'Longdistance_max': 10}
            Trk_dict= TC_Gen7_036
        elif timestamp =='122620':
            TC_Gen7_036 ={'NumPoints': 50, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 20, 'Longdistance_min':5, 'Longdistance_max': 8}
            Trk_dict= TC_Gen7_036
        elif timestamp =='134511':  
            TC_Gen7_036 ={'NumPoints': 50, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 9, 'SpeedOverGround_max': 14, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_036
        else:
            TC_Gen7_036 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 9, 'SpeedOverGround_max': 20, 'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_036
          
    elif file_name == 'TC_Gen7_037':
        TC_Gen7_037 ={'NumPoints': 4, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':2, 'SpeedOverGround_max': 50, 'Longdistance_min':-200, 'Longdistance_max': 200}
        Trk_dict= TC_Gen7_037



   #elif file_name == 'TC_Gen7_038':
  #  TC_Gen7_038 ={'NumPoints': 4, 'Latdistance_min': -10, 'Latdistance_max': 10,'SpeedOverGround_min':5, 'SpeedOverGround_max':50,'Longdistance_min':-200, 'Longdistance_max': 200}
  #  Trk_dict= TC_Gen7_038
    
    elif file_name == 'TC_Gen7_039':
        if timestamp == '143045':
            TC_Gen7_039 ={'NumPoints': 4, 'Latdistance_min': -10, 'Latdistance_max': 10, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 20,'Longdistance_min':-60, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_039
        elif timestamp == '143955':
            TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -100, 'Latdistance_max': 30, 'SpeedOverGround_min':2, 'SpeedOverGround_max': 100,'Longdistance_min':-200, 'Longdistance_max': 5}
            Trk_dict= TC_Gen7_039
        elif timestamp == '144112':
            #TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -100, 'Latdistance_max': 2, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 100,'Longdistance_min':-200, 'Longdistance_max': 5}
            TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -10, 'Latdistance_max': 10, 'SpeedOverGround_min':2, 'SpeedOverGround_max': 100,'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_039
        elif timestamp == '143659':
            TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':1, 'SpeedOverGround_max': 100,'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_039
        elif timestamp == '143330':
            TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -2.5, 'Latdistance_max': 0, 'SpeedOverGround_min':2, 'SpeedOverGround_max': 100,'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_039
        elif timestamp == '141746' or timestamp == '144243':
            TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -2.5, 'Latdistance_max': 0, 'SpeedOverGround_min':2, 'SpeedOverGround_max': 100,'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_039
        elif timestamp == '141514':
            TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 15,'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_039
        else:
            TC_Gen7_039 ={'NumPoints': 3, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 100,'Longdistance_min':-200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_039

    elif file_name == 'TC_Gen7_040':
        if timestamp == '140933' or timestamp == '143007':
            TC_Gen7_040 ={'NumPoints': 100, 'Latdistance_min': 2.5, 'Latdistance_max': 5, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min': 1, 'Longdistance_max': 200 } 
            Trk_dict= TC_Gen7_040
        else:
            TC_Gen7_040 ={'NumPoints': 100, 'Latdistance_min': -6, 'Latdistance_max': 6, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min': 1, 'Longdistance_max': 200 } 
            Trk_dict= TC_Gen7_040

    elif file_name == 'TC_Gen7_041': 
        if timestamp == '134053' or timestamp =='134315':
            TC_Gen7_041 ={'NumPoints': 200, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 13, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_041
        elif timestamp =='134524':
            TC_Gen7_041 ={'NumPoints': 400, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 13, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_041
        elif timestamp =='122617' or timestamp =='123042':
            TC_Gen7_041 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 20, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 15, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_041
        elif timestamp == '122834':
            TC_Gen7_041 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 20, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 15, 'Longdistance_min': -200, 'Longdistance_max': 20} 
            Trk_dict= TC_Gen7_041
        else:
            TC_Gen7_041 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':-1, 'SpeedOverGround_max': 15, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_041

    elif file_name == 'TC_Gen7_042': 
        if timestamp =='120942' or timestamp =='121059' or timestamp== '121249' or timestamp== '120053' or timestamp == '121946':
            TC_Gen7_042 ={'NumPoints': 100, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':10, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_042
        elif timestamp== '120606' :
            TC_Gen7_042 ={'NumPoints': 100, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':10, 'SpeedOverGround_max': 100, 'Longdistance_min': 2, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_042
        elif timestamp =='120438' :
            TC_Gen7_042 ={'NumPoints': 0, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 8, 'Longdistance_min': -8, 'Longdistance_max': 50} 
            Trk_dict= TC_Gen7_042
        elif timestamp =='120623' :
            TC_Gen7_042 ={'NumPoints': 1, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 7.5, 'Longdistance_min': -8, 'Longdistance_max': 50} 
            Trk_dict= TC_Gen7_042
        elif timestamp =='120254' :
            TC_Gen7_042 ={'NumPoints': 0, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 15, 'Longdistance_min': -20, 'Longdistance_max': 50} 
            Trk_dict= TC_Gen7_042
        else:
            TC_Gen7_042 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200} 
            Trk_dict= TC_Gen7_042
        
    elif file_name == 'TC_Gen7_043':
        TC_Gen7_043 ={'NumPoints': 50, 'Latdistance_min': -6, 'Latdistance_max': 2.5, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 25, 'Longdistance_min': -200, 'Longdistance_max': 200 }
        Trk_dict= TC_Gen7_043
  
    elif file_name == 'TC_Gen7_044':
        if timestamp == '145812':
            TC_Gen7_044 ={'NumPoints': 20, 'Latdistance_min': -2.5, 'Latdistance_max': 2, 'SpeedOverGround_min': 4, 'SpeedOverGround_max': 20, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_044
        elif timestamp == '150805':
            TC_Gen7_044 ={'NumPoints': 10, 'Latdistance_min': -20, 'Latdistance_max': 3, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_044
        elif timestamp == '145450' or timestamp =='145527' or timestamp =='145606':
            TC_Gen7_044 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 40, 'SpeedOverGround_min': 6, 'SpeedOverGround_max': 30, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_044
        elif timestamp == '150449' :
            TC_Gen7_044 ={'NumPoints': 10, 'Latdistance_min': -2.5, 'Latdistance_max': 2, 'SpeedOverGround_min': 6, 'SpeedOverGround_max': 30, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_044
        elif timestamp == '105236' or timestamp == '105814':
            TC_Gen7_044 ={'NumPoints': 30, 'Latdistance_min': -100, 'Latdistance_max': 5, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 17, 'Longdistance_min': -200, 'Longdistance_max': 150 }
            Trk_dict= TC_Gen7_044
        elif timestamp == '145917':
            TC_Gen7_044 ={'NumPoints': 50, 'Latdistance_min': -100, 'Latdistance_max': 5, 'SpeedOverGround_min': 10, 'SpeedOverGround_max': 17, 'Longdistance_min': -200, 'Longdistance_max': 150 }
            Trk_dict= TC_Gen7_044
        elif timestamp == '150724':
            TC_Gen7_044 ={'NumPoints': 10, 'Latdistance_min': -2.5, 'Latdistance_max': 2.5, 'SpeedOverGround_min': 1, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_044
        elif timestamp == '150644':
            TC_Gen7_044 ={'NumPoints': 10, 'Latdistance_min': -5, 'Latdistance_max': 5, 'SpeedOverGround_min': 15, 'SpeedOverGround_max': 40, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_044
        
        else:
            TC_Gen7_044 ={'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 5, 'SpeedOverGround_max': 17, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_044

    elif file_name == 'TC_Gen7_045':
        if timestamp == '112008'or timestamp == '112051':
            TC_Gen7_045 ={'NumPoints': 200, 'Latdistance_min': -40, 'Latdistance_max': -25,'SpeedOverGround_min':5, 'SpeedOverGround_max': 12, 'Longdistance_min': -50, 'Longdistance_max': 15}
            Trk_dict= TC_Gen7_045
        elif timestamp == '112131':
            TC_Gen7_045 ={'NumPoints': 100, 'Latdistance_min': -15, 'Latdistance_max': 0,'SpeedOverGround_min':5, 'SpeedOverGround_max': 6, 'Longdistance_min': -10, 'Longdistance_max': 10}
            Trk_dict= TC_Gen7_045
        else:
            TC_Gen7_045 ={'NumPoints': 100, 'Latdistance_min': -15, 'Latdistance_max': 0,'SpeedOverGround_min':4, 'SpeedOverGround_max': 10, 'Longdistance_min': -10, 'Longdistance_max': 10}
            Trk_dict= TC_Gen7_045
    
    elif file_name == 'TC_Gen7_046':
        if timestamp == '131433' or timestamp == '131544':
            TC_Gen7_046 ={'NumPoints': 40, 'Latdistance_min': -4, 'Latdistance_max': 4,'SpeedOverGround_min':6, 'SpeedOverGround_max': 20, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_046
        else:
            TC_Gen7_046 ={'NumPoints': 40, 'Latdistance_min': -4, 'Latdistance_max': 4,'SpeedOverGround_min':5, 'SpeedOverGround_max': 30, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_046
        
    elif file_name == 'TC_Gen7_047':
        if timestamp == '130320' or timestamp == '130521':
            TC_Gen7_047 ={'NumPoints': 4, 'Latdistance_min': 20, 'Latdistance_max': 100, 'SpeedOverGround_min':-1, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_047
        else:
            TC_Gen7_047 ={'NumPoints': 4, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':-1, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_047
    
    elif file_name == 'TC_Gen7_048':
        if timestamp == '145316':
            TC_Gen7_048 ={'NumPoints': 10, 'Latdistance_min': -4.5, 'Latdistance_max': 4.5, 'SpeedOverGround_min':4, 'SpeedOverGround_max': 7.5, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_048
        elif timestamp == '145752': 
            TC_Gen7_048 ={'NumPoints': 1, 'Latdistance_min': -10, 'Latdistance_max': 10, 'SpeedOverGround_min':3.5, 'SpeedOverGround_max': 20, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_048
        elif timestamp == '145121': 
            TC_Gen7_048 ={'NumPoints': 100, 'Latdistance_min': -10, 'Latdistance_max': 10, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_048
        else:
            TC_Gen7_048 ={'NumPoints': 10, 'Latdistance_min': -6, 'Latdistance_max': 6, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 7.4, 'Longdistance_min': -200, 'Longdistance_max': 200}
            Trk_dict= TC_Gen7_048

    elif file_name == 'TC_Gen7_049':
        if timestamp =='114352' or timestamp== '114451':
            TC_Gen7_049 ={'NumPoints': 6, 'Latdistance_min': -30, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 40, 'Longdistance_min': -25, 'Longdistance_max': -16 }
            Trk_dict= TC_Gen7_049
        elif timestamp == '115434':
            TC_Gen7_049 ={'NumPoints': 10, 'Latdistance_min': -20, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 40, 'Longdistance_min': -200, 'Longdistance_max': 3 }
            Trk_dict= TC_Gen7_049
        elif timestamp == '114252':
            TC_Gen7_049 ={'NumPoints': 10, 'Latdistance_min': -30, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 40, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_049
        elif timestamp == '115543':
            TC_Gen7_049 ={'NumPoints': 50, 'Latdistance_min': -30, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 5, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_049
        elif timestamp == '115721':
            TC_Gen7_049 ={'NumPoints': 20, 'Latdistance_min': 0, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 5, 'Longdistance_min': -20, 'Longdistance_max': 4 }
            Trk_dict= TC_Gen7_049
        elif timestamp== '143518':
            TC_Gen7_049 ={'NumPoints': 300, 'Latdistance_min': -30, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 40, 'Longdistance_min': -30, 'Longdistance_max': 12 }
            Trk_dict= TC_Gen7_049
        elif timestamp== '143853':
            TC_Gen7_049 ={'NumPoints': 200, 'Latdistance_min': 0, 'Latdistance_max': 30, 'SpeedOverGround_min': 4, 'SpeedOverGround_max': 5.5, 'Longdistance_min': -200, 'Longdistance_max': 4 }
            Trk_dict= TC_Gen7_049
        elif timestamp == '115254':  
            TC_Gen7_049 ={'NumPoints': 50, 'Latdistance_min': -30, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 40, 'Longdistance_min': -25, 'Longdistance_max': -10 }
            Trk_dict= TC_Gen7_049
        else:
            TC_Gen7_049 ={'NumPoints': 4, 'Latdistance_min': -30, 'Latdistance_max': 30, 'SpeedOverGround_min': 3, 'SpeedOverGround_max': 40, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_049

    elif file_name == 'TC_Gen7_050':
        if timestamp == '151045':
            TC_Gen7_050 ={'NumPoints': 50, 'Latdistance_min': -9, 'Latdistance_max': 5, 'SpeedOverGround_min': 19, 'SpeedOverGround_max': 30, 'Longdistance_min': -4, 'Longdistance_max': 4 }
            Trk_dict= TC_Gen7_050
        elif timestamp == '151200':
            TC_Gen7_050 ={'NumPoints': 100, 'Latdistance_min': -12, 'Latdistance_max': 0, 'SpeedOverGround_min': 1, 'SpeedOverGround_max': 20, 'Longdistance_min': -4.5, 'Longdistance_max': -2.5 }
            Trk_dict= TC_Gen7_050
        elif timestamp == '151327' : 
            TC_Gen7_050 ={'NumPoints': 100, 'Latdistance_min': -10, 'Latdistance_max': 0, 'SpeedOverGround_min': 2, 'SpeedOverGround_max': 30, 'Longdistance_min': -4, 'Longdistance_max': 0 }
            Trk_dict= TC_Gen7_050
        elif timestamp == '150854':
            TC_Gen7_050 ={'NumPoints': 200, 'Latdistance_min': -10, 'Latdistance_max': 0, 'SpeedOverGround_min': 1, 'SpeedOverGround_max': 100, 'Longdistance_min': -10, 'Longdistance_max': 0 }
            Trk_dict= TC_Gen7_050
        else:
            TC_Gen7_050 ={'NumPoints': 4, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min': 1, 'SpeedOverGround_max': 100, 'Longdistance_min': -200, 'Longdistance_max': 200 }
            Trk_dict= TC_Gen7_050

    elif file_name == 'TC_Gen7_051':
        if timestamp == '140515':
            TC_Gen7_051 ={'NumPoints': 100, 'Latdistance_min': -10, 'Latdistance_max': 10, 'SpeedOverGround_min': 2, 'SpeedOverGround_max': 10, 'Longdistance_min': -10, 'Longdistance_max': 6 }
            Trk_dict= TC_Gen7_051
        elif timestamp == '140417': 
            TC_Gen7_051 ={'NumPoints': 20, 'Latdistance_min': -10, 'Latdistance_max': 10, 'SpeedOverGround_min': 0, 'SpeedOverGround_max': 100, 'Longdistance_min': -5, 'Longdistance_max': 0 }
            Trk_dict= TC_Gen7_051
        else:
            TC_Gen7_051 ={'NumPoints': 20, 'Latdistance_min': -10, 'Latdistance_max': 10, 'SpeedOverGround_min': 0, 'SpeedOverGround_max': 100, 'Longdistance_min': -10, 'Longdistance_max': 6 }
            Trk_dict= TC_Gen7_051
    else: 
        Trk_dict= {'NumPoints': 20, 'Latdistance_min': -6, 'Latdistance_max': 6, 'SpeedOverGround_min':5, 'SpeedOverGround_max': 20, 'Longdistance_min': -20, 'Longdistance_max': 200 }
        #{'NumPoints': 10, 'Latdistance_min': -100, 'Latdistance_max': 100, 'SpeedOverGround_min':-1, 'SpeedOverGround_max': 100, 'Longdistance_min': -200}

    return Trk_dict 



def time_converter(df):
    time_smalles= df['TimeOrg'].min()
    df['Time']=  (df['TimeOrg'] - time_smalles)/1000000                                       #convert unit us to s 
    return df['Time']
    
def velocity_over_ground(df):
    df['Abstargetvelocity']= np.sqrt((df['Vx'] + df['VehicleVelocity'])**2 + df['Vy']**2)
    df['Abstargetvelocity']=  df['Abstargetvelocity']*(18/5)                                  #convert unit m/s to km/h
    return df['Abstargetvelocity']
    
def relative_velocity_values(df):
    df['AbsVelocity']= np.sqrt(df['Vx']**2 + df['Vy']**2) 
    df['AbsVelocity']=  df['AbsVelocity']*(18/5)                                              #convert unit m/s to km/h
    return df['AbsVelocity']
    
def travelling_direction_vector(df):    
    df['VectDirection']= np.cos(df["Heading"])
    return df['VectDirection']


def get_data(file):
    
    sdf = SdfReader(file)
    lib = sdf['/Resimulation/libWeGetASim']
    
    id = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['ul_ID']
    x  = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_ObjectCenter_m']['r4_X']
    y  = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_ObjectCenter_m']['r4_Y']
    vx = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Velocity_mps']['r4_X']
    vy = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Velocity_mps']['r4_Y']
    rx = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_RefPoint_m']['r4_X']
    ry = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_RefPoint_m']['r4_Y']
    h  = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['r4_Heading_rad']
    sx = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Size_m']['r4_X'] 
    sy = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Size_m']['r4_Y']
    tr = lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['b_ValidTrack']
    atr= lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['b_Accepted']
    acc= lib[:][1]['s_SDC_OutputSignals_s_SDC_RadarTrackCollection_as_RadarTracks']['s_Accel_mps2']['r4_Y']
    
    
    time_d = lib[:][0]
    
    veh_v       = lib[:][1]['s_SDC_OutputSignals_s_SDC_EgoVehicleDynamics']['r4_Velocity_mps']
    veh_Yawrate = lib[:][1]['s_SDC_OutputSignals_s_SDC_EgoVehicleDynamics']['r4_YawRate_Cond_radps']
    
    time_d = np.repeat(time_d,len(x[0]))

    veh_v       = np.repeat(veh_v,len(vx[0]))
    veh_Yawrate = np.repeat(veh_Yawrate,len(vx[0]))
    
    
    df = pd.DataFrame({'Id':id.flatten(),'X':x.flatten(), 'Y':y.flatten(), 'TimeOrg':time_d,
                      'Vx':vx.flatten(), 'Vy':vy.flatten(), 'Heading':h.flatten(), 'Rx':rx.flatten(), 'Ry':ry.flatten()
                       ,'Sx':sx.flatten() , 'Sy':sy.flatten(), 'Tr':tr.flatten(), 'A_Tr': atr.flatten()
                       , 'VehicleVelocity': veh_v.flatten(), 'VehicleYawRate': veh_Yawrate.flatten()
                       , 'Acceleration_X': acc.flatten()
                      })


    df['Time']               = time_converter(df)
    df['Abstargetvelocity']  = velocity_over_ground(df)
    df['AbsVelocity']        = relative_velocity_values(df)
    df['VectDirection']      = travelling_direction_vector(df)
    
    df = df[(df["X"]!=0) & (df["Y"]!=0) & (df["Id"]!=0) & (df["Vx"]!=0)  & (df["Vy"]!=0) 
                & (df["Heading"]!=0) & (df["Rx"]!=0) & (df["Ry"]!=0) & (df["Sx"]!=0)& (df["Sy"]!=0) 
           ]  #&(df["Tr"]!=0) &(df["A_Tr"]!=0)   

         
    df_grps = df.groupby(['Id'])
    
    return df_grps, df




def get_trk_IDs(file):
    Id_list = []
    df_grps,df = get_data(file)
    Id_list.clear()             
    
    filename= Path(file).stem

    Sel_dict = selection_criteria(filename)
    print(Sel_dict.values())
    
    #precuts ==> select good tracks:
    for group_name, df_group in df_grps:
        NumPoints        =  len(df_group)                                           #Number of points in each track
        Latdistance      =  df_grps.get_group(group_name)['Y'].mean()               #Lateral distance should not be more than 10m
        Longdistance     =  df_grps.get_group(group_name)['X'].mean()
        HeadingAng       =  df_grps.get_group(group_name)['Heading'].mean()
        SpeedOverGround  =  df_grps.get_group(group_name)['Abstargetvelocity'].mean()
        Longdistance     =  df_grps.get_group(group_name)['X'].mean()
        latSpeed         =  df_grps.get_group(group_name)['Vy'].mean()
        len_size         =  df_grps.get_group(group_name)['Sx'].mean()
        TargtSpeed       =  df_grps.get_group(group_name)['AbsVelocity'].mean()
        AcceptedTrk      =  df_grps.get_group(group_name)['A_Tr'].mean()
       
        
        if(NumPoints > Sel_dict['NumPoints'] and abs(Latdistance) < Sel_dict['Latdistance_max']  and abs(Latdistance) > Sel_dict['Latdistance_min']
         and abs(SpeedOverGround) > Sel_dict['SpeedOverGround_min'] and abs(SpeedOverGround) <=  Sel_dict['SpeedOverGround_max']
         and Longdistance > Sel_dict['Longdistance_min'] and Longdistance < Sel_dict['Longdistance_max']):
         #and len(df_group[df_group['A_Tr'] == 1] > 0)):  
 
            Id_list.append(group_name)
            
    return df_grps,df, Id_list 

def get_files(path,ext):
    """get all files with extension ext in path 
    Args:
        path (str): path to search files in
        ext (str): extension of files
    Returns:
        list: list of strings of absolute paths to files
    """    
    file_lst = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            if name.endswith(ext):
                file_lst.append(os.path.join(path, name))
    return file_lst

def print_track_info(file,sdf_df,Ids_list):
    """Create Dataframe with valid tracks and their features respectively 
    Args:
        file (str): string file name
        sdf_df (df): dataframe which contains track signals
        Ids_list(list): List of valid Id tracks
    Returns:
        DF: DataFrame with the info for each valid track.  
    """ 
   
    df_track_info = pd.DataFrame(columns = ['Test_Scenario', 'Test_No', 'DateTime','Track_No','Distance(m)','Duration(s)','X1(m)','X2(m)','Y1(m)','Y2(m)'])
    find_string = "TC_Gen7_"
    outstring = ""
    split_filename = file[file.find(find_string) + len(find_string):].split('_')
    test_no = split_filename[0]
    sub = split_filename[1]
    datetime = split_filename[2] + '_' + split_filename[3] + '_' + split_filename[4] + '_' + split_filename[5]
    test_info_string = test_no + ',' + sub + ',' + datetime + ','
    #df_grps, df, Ids_list= get_trk_IDs(file)
    for track_id in Ids_list:
        df_tmp = sdf_df[sdf_df['Id'] == track_id]
        x1_m = df_tmp.iloc[0]['X']
        x2_m = df_tmp.iloc[-1]['X']
        y1_m = df_tmp.iloc[0]['Y']
        y2_m = df_tmp.iloc[-1]['Y']
        track_distance_m = math.sqrt((x2_m - x1_m)**2 + 
            (y2_m - y1_m)**2)
        duration_s = df_tmp.iloc[-1]['Time'] - df_tmp.iloc[0]['Time']
        if(track_distance_m >= 10 and duration_s > 5 and len(df_tmp[df_tmp['A_Tr'] == 1]) > 0):

            df_track_info = df_track_info.append({'Test_Scenario':int(test_no), 'Test_No': int(sub), 'DateTime':datetime,
                                                  'Track_No':track_id,'Distance(m)':round(track_distance_m,2),'Duration(s)':duration_s,'X1(m)':round(x1_m,2),'X2(m)':round(x2_m,2),'Y1(m)':round(y1_m,2),'Y2(m)':round(y2_m,2)}, ignore_index = True)
    return df_track_info


def CreateFilePath(input_path):
    dst_path = os.path.join(input_path, "Report")
    clean_folder(dst_path)
    try:
        
        os.makedirs(dst_path)
        os.makedirs( os.path.join(dst_path, "Plots"))
        
    except:
        if(os.path.exists(dst_path)):
            print('Directory already exists')
        else:
            print("Directory couldn't be created. Check Admin Rights")
            return 
    
    return dst_path

def clean_folder(Plots_Dir):
    # Delete folder if exists and create it again
    try:
        shutil.rmtree(Plots_Dir)
        #os.mkdir(Plots_Dir)
        
    except FileNotFoundError:
        #os.mkdir(Plots_Dir)
        print('Directory Not Found')


def position_plots(df_grps,Ids_list):

    adjust_scale = False
    adjust_Yscale = False
    fig, axes = plt.subplots(nrows=3, ncols=2,figsize=(9.5,12), constrained_layout = True)
    temp = 0
    
    
    #fig.suptitle(str(file_name)+'.sdf' , fontsize=16)
    min_val = 0xFFFFFF

    for i in range(len(Ids_list)):
        df_grps.get_group(Ids_list[i]).plot(x='Time',y='X',linestyle='-', marker='o',c=color[i % len(color)],markersize = MARKSIZE, ax=axes[0, 0],legend=None) #, label= 'Id= ' + str(Id_list[i])
        #df_grps.get_group(Ids_list[i]).plot.scatter(x='Time',y='Ry',c=color[i % len(color)],s=10, ax=axes[0, 1], ylabel='Object Position X (m)', xlabel='Object Position Y (m)',colorbar=False) 
        df_grps.get_group(Ids_list[i]).plot(x='Y',y='X',linestyle='-', marker='o',c=color[i % len(color)],markersize = MARKSIZE,ax=axes[0, 1],legend=None)

        df_grps.get_group(Ids_list[i]).plot(x='Time',y='Abstargetvelocity',linestyle='-', marker='o',c=color[i % len(color)],markersize = MARKSIZE,ax=axes[1, 0],legend=None)
        df_grps.get_group(Ids_list[i]).plot(x='Time',y='VectDirection',linestyle='-', marker='o',c=color[i % len(color)],markersize = MARKSIZE,ax=axes[1, 1],legend=None)

        df_grps.get_group(Ids_list[i]).plot(x='Time',y='Sx',linestyle='-', marker='o',c=color[i % len(color)],markersize = MARKSIZE,ax=axes[2, 0],legend=None)
        df_grps.get_group(Ids_list[i]).plot(x='Time',y='Sy',linestyle='-', marker='o',c=color[i % len(color)],markersize = MARKSIZE,ax=axes[2, 1],legend=None)
        #df_grps.get_group(Ids_list[i]).plot.scatter(x='Rx',y='Ry',c=color[i % len(color)],s=10,ax=axes[1, 1], colorbar=False)
        #if(abs(max(df_grps.get_group(Ids_list[i])['Rx']) - min(df_grps.get_group(Ids_list[i])['Rx'])) < 4 and ( abs(max(df_grps.get_group(Ids_list[i])['Rx'])) < 10 or abs(min(df_grps.get_group(Ids_list[i])['Rx'])) < 10)):
        if(min(df_grps.get_group(Ids_list[i])['X']) < min_val):
            min_val = min(df_grps.get_group(Ids_list[i])['X'])
        
        if(abs(max(df_grps.get_group(Ids_list[i])['Rx']) - min(df_grps.get_group(Ids_list[i])['Rx'])) > temp):
            temp = abs(max(df_grps.get_group(Ids_list[i])['Rx']) - min(df_grps.get_group(Ids_list[i])['Rx']))
        
        if(abs(max(df_grps.get_group(Ids_list[i])['Y'])- min(df_grps.get_group(Ids_list[i])['Y'])) < 10):
            adjust_Yscale = True
        
    if(min_val > 0 and temp < 10):
        adjust_scale = True

    
    axes[0,0].set_ylabel('Object Point Position X (m)',fontdict={'fontsize':15})
    axes[0,0].set_xlabel('Time (s)',fontdict={'fontsize':15})
    axes[0,0].grid()
    if(adjust_scale):
        axes[0,0].set_ylim(-20,20)
    #axes[0,0].set_xlim(30,50)

  
    axes[0,1].set_ylabel('Object Point Position X (m)',fontdict={'fontsize':15})
    axes[0,1].set_xlabel('Object Point Position y (m)',fontdict={'fontsize':15})
    #axes[0,1].set_ylim(-10,10)
    axes[0,1].grid()
    
    if(adjust_scale):
        axes[0,1].set_ylim(-20,20)
    if(adjust_Yscale):
        axes[0,1].set_xlim(-10,10)

 
    
    axes[1,0].set_ylabel('Object Velocity (km/h)',fontdict={'fontsize':15})
    axes[1,0].set_xlabel('Time (s)',fontdict={'fontsize':15})
    axes[1,0].grid()

    
    axes[1,1].set_ylabel('Traveling Direction Vector',fontdict={'fontsize':15})
    axes[1,1].set_xlabel('Time (s)',fontdict={'fontsize':15})
    axes[1,1].grid()

    axes[2,0].set_ylabel('Object Length (m)',fontdict={'fontsize':15})
    axes[2,0].set_xlabel('Time (s)',fontdict={'fontsize':15})
    axes[2,0].grid()

    axes[2,1].set_ylabel('Object Width(m)',fontdict={'fontsize':15})
    axes[2,1].set_xlabel('Time (s)',fontdict={'fontsize':15})
    axes[2,1].grid()

    return fig




def ReportGen(sdf_path):

    list_plots = []
    list_sdf_notracksfound = []

    out_path = CreateFilePath(sdf_path)
    sdf_files = get_files(sdf_path, ".sdf")
    df_full_trackinfo = pd.DataFrame()
    with alive_bar(len(sdf_files)) as bar:
        for file in sdf_files:
            logger.info("Processing SDF: {}".format(Path(file).stem))
            df_grps, df, Ids_list= get_trk_IDs(file)
            df_track_info = print_track_info(file,df,Ids_list)
            df_full_trackinfo = pd.concat([df_full_trackinfo, df_track_info], ignore_index=True, sort=False)

            if(Ids_list == []):
                logger.warning(
                    "Couldn't process {} as it didn't have valid track".format(Path(file).stem)
                )

                list_sdf_notracksfound.append(Path(file).stem)
                pass
            else:
                file_name = Path(file).stem
                fig = position_plots(df_grps,Ids_list)

                fig.savefig(os.path.join(out_path,'Plots',file_name + '.png'))
                list_plots.append(os.path.join(out_path,'Plots',file_name + '.png'))

                plt.close(fig)
            bar()

    df_full_trackinfo.to_csv(os.path.join(out_path, "track_info.csv"),index=False)


    pdf = FPDF() 
    for plot_img in list_plots:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 15)
        #pdf.cell(0, 10, Path(plot_img).stem, 1, 1)
        pdf.cell(0, 10, Path(plot_img).stem, align='C')
        
        pdf.image(plot_img, 10, 30, 190)
    shutil.rmtree(os.path.join(out_path,'Plots'))

    if(list_sdf_notracksfound != []):

        filename = os.path.join(out_path, "Files_NotTracked_Log.txt")
        with open(filename, 'w+') as f:
            f.write("The Following SDF Files din't have any track accepted\n")
     
            # write elements of list
            for items in list_sdf_notracksfound:
                f.write('%s\n' %items)
     
    print("File written successfully")

   
    pdf.output(os.path.join(out_path, "Report.pdf"), 'F')
    logger.info("Output Files created at: {}".format(out_path))

        
        
            

if __name__ == "__main__":

    #sdf_path = r'C:\\sndboxes\\gogeta\\avengers-initiative-gogeta\\Data\\SDFs_run_2022_10_07\\'
    sdf_path = r'C:\\Users\\z0181875\\Documents\\python_workspace\\Performance_Report\\Data\\Manuel\\'
    #sdf_path = r"C:\\Users\\z0181875\\Documents\\python_workspace\\Performance_Report\Data\\\SDFs_run_2022_09_30-16_54_21\\"
    ReportGen(sdf_path)

    



