from shutil import SameFileError
import networkx as nx
import json
import r2pipe, os, sys, time, csv
import numpy as np
import pandas as pd
import signal
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from graphviz import Digraph
import pydot
from networkx.drawing import nx_agraph
import torch
import csv,random
from tqdm import tqdm


#Result=[],
Dataset={}

# #找ELF file path
# def ELF_p(file):
#     cmd='find /mnt/database0/linuxmal -name "'+file+'" -type f' 
#     find_path=list(os.popen(cmd))[0] 
#     find_path=find_path.replace('\n','') 
#     return find_path

# def ELF_p(file):
#     return '/mnt/database0/linuxmal/'+file[:2]+'/'+file
def ELF_p(file):
    return './binary/'+file


#透過r2.cmd('afl)找所有Function
def radare2_get_function(r2):
    func=r2.cmd('afl')
    function=[]
    for lines in func.split('\n'):
        for word in lines.split():
            if word[0].isalpha():
                function.append(word)
    return function

#透過r2.cmd('pifj')找到function之json，並且透過dict搜尋該function之opcode
def radare2_get_function_opcode(r2,function,name):
    for f in function:
        try:
            if f[:3]=='fcn':
                #print(f)
                r2.cmd('s '+str(f))
                json=r2.cmdj('pifj')
                tmp=[]
                for i in range(len(json['ops'])):
                    tmp.append(json['ops'][i]['opcode'].split(' ')[0])
                #print(tmp)
                np.save('./DetectionUserDefined/'+f+'_'+name, tmp)
                print('---')
        except:
            pass
            print('Collect error!')

#找每支file中每個function之 opcode，並且儲存成npy格式
def radare2_analysis(file,path,name):
    r2=r2pipe.open(path)
    r2.cmd('aaaa')
    function=radare2_get_function(r2)
    radare2_get_function_opcode(r2,function,name)

        
def read_label():
    # read label file
    label_dict = {'BenignWare':0, 'Mirai':1, 'Tsunami':2, 'Hajime':3, 'Dofloo':4, 'Bashlite':5, 'Xorddos':6, 'Android':7, 'Pnscan':8, 'Unknown':9}
    label = {}
    threshold = {}
    with open('/home/connlab/ChiaYi/CFGtest/CFG/dataset.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        next(rows)
        for row in rows:
            threshold[row[0]] = row[2]
            label[row[0]] = label_dict[row[1]]
    print('---- finish read label ----\n')
    return label

def main():
    Malware_path='./cfg_output/'
    #Sample=np.load('Benignware.npy')
    for dirPath,dirNames,fileNames in os.walk(Malware_path):
        fileNames.sort()
        for index,f in enumerate(fileNames):
            name=f.replace('.dot','')
            #if name in Sample:
            try:
                #print(index,f)
                with open('Recording_num2.txt', 'a') as f:
                    f.write(str(index)+'\n')
                f.close()
                fpath=ELF_p(name)#找file path
                print(fpath)
                radare2_analysis(name,fpath,name)#透過radare2 進行分析
            except:
                pass
            #else:
                #continue
        


if __name__=='__main__':
    main()
