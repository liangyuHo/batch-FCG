import sklearn
import pickle
from param_parser import parameter_parser
import numpy as np


def main(args):
    model_type = args.model
    model = pickle.load(open('./Model_save/'+model_type+'.pkl','rb'))
    
    feature = np.load('../feature/feature.npy')
    print(feature)
    label = model.predict(feature)
    print(label)
    

if __name__=='__main__':
    args = parameter_parser()
    main(args)
