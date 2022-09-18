
import numpy as np

class ComponentParser():
    def __init__(self):
        pass




class DictVect():
    def __init__(self,features,expected_values):
        self.feature_map={f: idx for idx,f in enumerate(features)} 
        self.expected_vals={f:v for f,v in zip(features,expected_values)}
        self.train_vecs=None
        self.labels=None

    def train(self,vec_labels):
        vecs,labels=[],[]
        for vec,label in vec_labels:
            vecs.append(vec)
            labels.append(label)
        self.train_vecs=np.array(vecs)  
        self.labels=labels

    def getFeature(self,vec_map,dev):
        """
        if deviation with in or near 1 consider else 0
        """
        size=len(self.feature_map)
        arr=[0]*size
        for k,v in vec_map.items():
            exp_val=self.expected_vals[k]
            if v<= exp_val+dev and v>=exp_val-dev:
                arr[self.feature_map[k]]=1
        return np.array(arr).reshape(1,size)

    def predict(self,vec_map,dev=0.05):
        vec=self.getFeature(vec_map,dev)
        matches=np.dot(self.train_vecs,vec.T)
        matches=matches.ravel()
        best_idx=np.argmax(matches)
        count=np.count_nonzero(self.train_vecs[best_idx])
        score=matches[best_idx]/count
        return self.labels[best_idx],score

