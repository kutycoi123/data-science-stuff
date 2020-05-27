import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter
import sys

def to_datetime(str):
    """Convert str to python datetime"""
    return pd.Timestamp(str).to_pydatetime()

def main():
    filename = sys.argv[1]
    cpu_data = pd.read_csv(filename)
    cpu_data['timestamp'] = cpu_data.apply(lambda x: to_datetime(x['timestamp']), axis=1)
    # Loess
    loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac=0.02)
    # Kalman
    kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]

    initial_state = kalman_data.iloc[0]

    observation_covariance = np.diag([0.5,  2,   0.3    ,60]) ** 2
    transition_covariance = np.diag( [0.01, 0.1, 0.03  ,7]) ** 2
    transition_matrix = [[0.97,0.5,0.2,-0.001],[0.1,0.4,2.2,0],[0,0,0.95,0],[0,0,0,1]]
    kf = KalmanFilter(
        initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition_matrix
        )
    kalman_smoothed, _ = kf.smooth(kalman_data)

    #Reference: https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html
    fig, (ax1,ax2) = plt.subplots(2, figsize=(12, 5), sharex=True)
    ax1.set_title("Loess")
    ax1.plot(cpu_data['timestamp'].values, cpu_data['temperature'].values, 'b.', alpha=0.5)
    ax1.plot(cpu_data['timestamp'].values, loess_smoothed[:, 1], 'r-')

    ax2.set_title("Kalman")
    ax2.plot(cpu_data['timestamp'].values, cpu_data['temperature'].values, 'b.', alpha=0.5)
    ax2.plot(cpu_data['timestamp'].values, kalman_smoothed[:, 0], 'r-')
    fig.savefig('cpu.svg')
    #plt.show()
    
if __name__ == "__main__":
    main()
