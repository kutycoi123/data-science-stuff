import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

def index_of_lowest_total_precipitation():
    annual_totals_by_cities = np.sum(totals, axis=1)
    return np.argmin(annual_totals_by_cities)

def get_monthly_average_precipitation():
    monthly_totals = np.sum(totals, axis=0)
    monthly_counts = np.sum(counts, axis=0)
    return monthly_totals / monthly_counts
    
def get_daily_average_precipitation():
    annual_totals_by_cities = np.sum(totals, axis=1)
    annual_counts_by_cities = np.sum(counts, axis=1)
    return annual_totals_by_cities/annual_counts_by_cities

def get_quaterly_total_precipitation():
    totals_reshaped = np.transpose(totals)
    first_quater_total = np.sum(totals_reshaped[0:3, :], axis=0)
    second_quater_total = np.sum(totals_reshaped[3:6, :], axis=0)
    third_quater_total = np.sum(totals_reshaped[6:9, :], axis=0)
    fourth_quater_total = np.sum(totals_reshaped[9:, :], axis=0)
    result = np.vstack((first_quater_total, second_quater_total, third_quater_total, fourth_quater_total))
    return np.transpose(result)

print("Row with lowest total precipitation:")
print(index_of_lowest_total_precipitation())

print("Average precipitation in each month:")
print(get_monthly_average_precipitation())

print("Average precipitation in each city:")
print(get_daily_average_precipitation())

print("Quarterly precipiration totals:")
print(get_quaterly_total_precipitation())
