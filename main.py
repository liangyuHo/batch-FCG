import r2pipe, os, sys, time, csv
from param_parser import parameter_parser
#import AnalysisUserDefined
#import CreateRenameGraph
import pandas as pd
import numpy as np




def main(args):
    cmd = 'mkdir ./Redefine/ ./DetectionUserDefined/ ./cfg_output/'
    os.system(cmd)
    cmd = 'python CG_extract.py'
    os.system(cmd)
    cmd = 'python graph2vec.py --input-path ./cfg_output/ --output-path ./tmp.csv'
    os.system(cmd)
    cmd = 'python AnalysisUserDefined.py'
    os.system(cmd)
    cmd = 'fdupes -r ./DetectionUserDefined/ > ./fdupes.txt'
    os.system(cmd)
    cmd = 'python CreateRenameGraph.py'
    os.system(cmd)
    cmd = 'python graph2vec+.py --input-path ./Redefine/ --output-path ./test.csv'
    os.system(cmd)
    
    feature=[]
    data = pd.read_csv('./test.csv',header=None)
    print(data.shape[0])
    for i in range(data.shape[0]):
        tmp = data.iloc[i,1:132].values.tolist()
        feature.append(tmp)
    feature = np.array(feature)
    print(feature)
    np.save('./feature/feature',feature)
    cmd = 'rm -rf ./Redefine/ fdupes.txt ./DetectionUserDefined/  tmp.csv test.csv ./cfg_output/'
    os.system(cmd)

if __name__=='__main__':
    args = parameter_parser()
    main(args)
