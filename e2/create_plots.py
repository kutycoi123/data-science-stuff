import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    df1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
                        names=['lang', 'page', 'views', 'bytes'])
    df2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
                      names=['lang', 'page', 'views', 'bytes'])

    df2['day1_views'] = df1['views']
    df1.sort_values(by=['views'], inplace=True,ascending=False)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1,2,1)
    plt.xlabel("Rank")
    plt.ylabel("Views")
    plt.title("Popularity Distribution")
    plt.plot(df1['views'].values)
    
    plt.subplot(1,2,2)
    plt.xlabel("Day 1 views")
    plt.ylabel("Day 2 views")
    plt.title("Daily Correlation")
    plt.plot(df2['day1_views'].values, df2['views'].values, 'bo')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('wikipedia.png')
#    plt.show()
if __name__ == "__main__":
    main()
