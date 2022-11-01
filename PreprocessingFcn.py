from os import replace
import pandas as pd
import numpy as np
import csv

def Read_similar_opcode_fcn(path):
    Similar_sample={}
    with open(path, 'r') as myfile:
        repeat=myfile.read()
    Groups=[]
    c=0
    tmp=[]
    for index,lines in enumerate(repeat.split('\n')):
        if lines!='':
            c=c+1
            name=lines.replace('./','')
            name=name.replace('.npy','')
            tmp.append(name)
        else:
            Groups.append(tmp)
            tmp=[]
    #Groups=np.array(Groups)
    print(len(Groups))
    for group in Groups:
        try:
            replacement=group[0][:12]
            #print(replacement)
            for index,item in enumerate(group):
                    Similar_sample[item]=replacement
        except:
            pass
    # for key,value in Similar_sample.items():
    #     print(key,value)
    return Similar_sample

def Classify_same_opcode_sequence(path):
    Similar_sample={}
    with open(path, 'r') as myfile:
        repeat=myfile.read()
    Groups=[]
    c=0
    tmp=[]
    for index,lines in enumerate(repeat.split('\n')):
        if lines!='':
            tmp.append(lines[lines.index('/')+1:lines.index('/')+13])
        else:
            Groups.append(tmp)
            tmp=[]
    print(len(Groups))
    for group in Groups:
        try:
            replacement=group[0]
            for index,item in enumerate(group):
                    Similar_sample[item]=replacement
        except:
            pass
    return Similar_sample
            

def main():
    #dict=Read_similar_opcode_fcn('/mnt/database0/Rooted_n_gram/classification/Rename.txt')
    dict=Classify_same_opcode_sequence('/mnt/database0/Rooted_n_gram/classification/DetectionUserDefined.txt')

        

if  __name__=='__main__':
    main()
