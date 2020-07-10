import sys
import time
import numpy as np
import pandas as pd
from implementations import all_implementations

N_ARRAYS = 50
N_ELEM = 10000
MAX_ELEM = 100

def gen_random_arrays():
    np.random.seed(1)
    arrs = []
    for _ in range(N_ARRAYS):
        tmp = []
        for _ in range(N_ELEM):
            tmp.append(np.random.randint(MAX_ELEM))
        arrs.append(tmp)
    return np.array(arrs)

def main():
    rand_arrs = gen_random_arrays()
    data = {'qs1':[],'qs2':[],'qs3':[],'qs4':[],'qs5':[],
            'merge':[],'partition_sort':[]}
    sort_names = ['qs1','qs2','qs3','qs4','qs5','merge','partition_sort']
    for rand_arr in rand_arrs:
        for idx,sort in enumerate(all_implementations):
            start = time.time()
            res = sort(rand_arr)
            end = time.time()
            data[sort_names[idx]].append(end-start)
    data_df = pd.DataFrame(data)
    data_df.to_csv('data.csv', index=False)
    
if __name__ == "__main__":
    main()
