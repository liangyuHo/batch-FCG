from cProfile import label
import numpy as np
import pandas as pd
import networkx as nx
import csv,os
import PreprocessingFcn
import time

start = time.time()
Rename=PreprocessingFcn.Read_similar_opcode_fcn('./fdupes.txt')
end = time.time()
print('Read Rename Dict:',end - start)

def Re_create(path,filename):
    with open(path,'r') as file:
        data=file.read()
    label={}
    G=nx.DiGraph() 
    for lines in data.split('\n'):
        tmp=[]
        for words in lines.split():
            if words[0]=='"':
                words=words.replace('"','')
            tmp.append(words)
        try:
            if tmp[1][1]=='l':
                func=tmp[1][7:]
                func=func.replace('"','')
                if func[:3]=='fcn':
                    label[tmp[0]]=Rename[func+'_'+filename]
                else:
                    label[tmp[0]]=func #addr =function name
        except:
            pass
    for lines in data.split('\n'):
        tmp=[]
        for words in lines.split():
            #print(words)
            if words[0]=='"':
                words=words.replace('"','')
            tmp.append(words)
        try:
            if tmp[1]=='->':
                G.add_edge(label[tmp[0]],label[tmp[2]])
        except:
            pass
    #print(nx.info(G))
    name=path.replace('./cfg_output/','')
    nx.drawing.nx_pydot.write_dot(G, './Redefine/'+name)

def build_graph(path):
    with open(path,'r') as file:
        data=file.read()
    G=nx.DiGraph()
    for lines in data.split('\n'):
        print(lines)
        try:
            if lines[15]=='-':
                G.add_edge(lines[1:13],lines[19:31])
        except:
            pass
    return G

def main():
    Malware_path='./cfg_output/'
    for dirPath,dirNames,fileNames in os.walk(Malware_path):
        fileNames.sort()
        for index,f in enumerate(fileNames):
            fpath=dirPath+f
            filename=f.replace('.dot','')
            print(index,f)
            Re_create(fpath,filename)

if __name__=='__main__':
    start = time.time()
    main()
    end = time.time()
    print('Redraw Graph:',end - start)
