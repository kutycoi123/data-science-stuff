import sys
import time
import numpy as np
import pandas as pd
from implementations import all_implementations

N_ARRAYS = 50
N_ELEM = 25000
MAX_ELEM = 2000

def gen_rand_arr():
    return np.random.randint(0, MAX_ELEM, N_ELEM)
def main():
    data = {'qs1':[],'qs2':[],'qs3':[],'qs4':[],'qs5':[],
            'merge':[],'partition_sort':[]}
    sort_names = ['qs1','qs2','qs3','qs4','qs5','merge','partition_sort']
    for _ in range(N_ARRAYS):
        rand_arr = gen_rand_arr()
        for idx,sort in enumerate(all_implementations):
            start = time.time()
            res = sort(rand_arr)
            end = time.time()
            data[sort_names[idx]].append(end-start)  
    data_df = pd.DataFrame(data)
    data_df.to_csv('data.csv', index=False)    

if __name__ == "__main__":
    main()
