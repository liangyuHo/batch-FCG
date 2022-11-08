import sklearn
import pickle
from param_parser import parameter_parser
import numpy as np


def main(args):
    model_type = args.model
    model = pickle.load(open('./Model_save/'+model_type+'.pkl','rb'))
    
    feature = np.load('../feature/feature.npy',allow_pickle=True)
    name = feature[-1]
    feature = np.delete(feature,-1)
    test = []
    for i in feature:
        test.append(i)
    
    test = np.array(test)
    label = model.predict(test)

    for i,j in zip(name,label):
        print(i,j)

    

if __name__=='__main__':
    args = parameter_parser()
    main(args)
