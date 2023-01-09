import networkx as nx
import json
import r2pipe, os, sys, time, csv
import numpy as np
import signal
from networkx.readwrite import json_graph
import os
import shutil
#import Filelist
import warnings
import csv


def radare(fname,target,name):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(30)
    r2 = r2pipe.open(fname)
    start = time.time()
    try:
        r2.cmd('aaaa')
    except Exception:
        print('time out')
        pid = os.popen("ps aux | grep " + fname+ " | grep -v grep | awk '{print $2}'")
        for i in pid:
            os.popen("kill -9 " + i.strip('\n'))
            continue
        return
    cmd_of_save_dot='agCd >> '+target+'/'+name+'.dot'
    #cmd_of_save_dot='agCd >'+name+'.dot'
    r2.cmd(cmd_of_save_dot)
    end = time.time()
    return end-start
    
    #return call_graph_list

def signal_handler(signum, frame):
    raise Exception("Timed out!")

'''
def main():
    #elf_type = ['benignware', 'linuxmal']

    success_list=Filelist.Filelist()
    success_folder=Filelist.Folderlist()
    elf_type = ['linuxmal']
    
    index=0
    for i in elf_type:
        ELF_path = '/mnt/database0/' + i
        for dirPath, dirNames, fileNames in os.walk(ELF_path):
            if dirPath[-1:0] in success_folder:
                continue
            fileNames.sort()
            for f in fileNames:
                if f not in success_list:
                    print(index)
                
                    p=dirPath.replace('/mnt/database0/','')
                    target='/home/connlab/ChiaYi/CFGtest/CFG/PSI_graph/Call_graph/'+p
                    try:
                        os.makedirs(target)
                    except:
                        pass
                    path=dirPath+'/'+f
                    print(path)
                    signal.signal(signal.SIGALRM, signal_handler)
                    signal.alarm(30)
                    try:
                        CG_dot=radare(path,target,f)
                        index=index+1
                    except Exception:
                        print("Timed out!")
                        txt=open('skip.txt','a')
                        txt.write(f+'\n')
                        txt.close
    
                #json.dump(CG_json, open(target+'/'+f+'.json', 'w'))
'''

def main():
    sys.setrecursionlimit(100000000)
    #list=Filelist.Filelist()
    #folder=Filelist.ExtractFolder(list)
    elf_type = ['ELF_Analyze']
    #elf_type = ['linuxmal']
    
    
    feature_vec = {}
    timelist = [['filename','time']]

    count = 0
    print('gege')
    for i in elf_type:
        ELF_path = './' + i
        for dirPath, dirNames, fileNames in os.walk(ELF_path):
            fileNames.sort()
            
            print('Extracting CFG from', dirPath)
            for f in fileNames:
                
                #if f in list:
                #    continue
                
                if count % 10000 == 0:
                    print('extract %d files' % count)
                try:
                    file_dir = f[:2]
                    call_graph_list = []
                    fname = os.path.join(dirPath, f)
                    path = fname
                    #path = fname.replace('/mnt/database0/', './call_graph_list/')
                    if f.find('.o') != -1:
                        continue
                        
                    if not os.path.isfile(path + '.json'):
                       
                        print(count, f)
                        signal.signal(signal.SIGALRM, signal_handler)
                        signal.alarm(60)
                        filesource=dirPath+'/'+f
                        
                        try:
                            target='./cfg_output/'
                            passtime = radare(filesource,target,f)
                            count=count+1
                            timelist.append([f,passtime])
                            #if count == 10:
                            #    print(os._exit(0))
                        except Exception:
                            print("Timed out!")
                            pid = os.popen("ps aux | grep " + fname+ " | grep -v grep | awk '{print $2}'")
                            for i in pid:
                                os.popen("kill -9 " + i.strip('\n'))
                                continue
                            print('success kill')
                        
                        
                        #if 'linuxmal' in dirPath:
                        #    if not os.path.isdir('call_graph_list/linuxmal/' + file_dir):
                        #        os.popen('mkdir call_graph_list/linuxmal/' + file_dir)

                        #elif 'benignware' in dirPath:
                        #    if not os.path.isdir('call_graph_list/benignware/' + file_dir):
                        #        os.popen('mkdir call_graph_list/benignware/' + file_dir)

                        #if call_graph_list != []:
                        #    json.dump(call_graph_list, open(path + '.json', 'w'))
                        #    count += 1
                        
                except:
                    print(f, 'error')
    
    
    with open('time.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(timelist)

if __name__=='__main__':
    main()
