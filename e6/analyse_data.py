import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data_file = 'data.csv'


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        data_file = sys.argv[1]

    data = pd.read_csv(data_file)
    melt = pd.melt(data)
    anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge'], data['partition_sort'])
    print("anova p-value:", anova.pvalue)
    posthoc = pairwise_tukeyhsd(melt['value'], melt['variable'], alpha=0.05)
    print("post hoc analysis:")
    print(posthoc)
    print("qs1 mean:", data['qs1'].mean())
    print("qs2 mean:", data['qs2'].mean())
    print("qs3 mean:", data['qs3'].mean())
    print("qs4 mean:", data['qs4'].mean())
    print("qs5 mean:", data['qs5'].mean())
    print("merge mean:", data['merge'].mean())
    print("partion_sort mean:", data['partition_sort'].mean())
    


