import pandas as pd


totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

def index_of_lowest_total_precipitation():
    annual_totals = totals.sum(axis=1)
    return annual_totals.idxmin(axis=0)

def get_monthly_average_precipitation():
    monthly_totals = totals.sum(axis=0)
    monthly_counts = counts.sum(axis=0)
    return monthly_totals.div(monthly_counts)

def get_daily_average_precipitation():
    annual_totals_by_cities = totals.sum(axis=1)
    annual_counts_by_cities = counts.sum(axis=1)
    return annual_totals_by_cities.div(annual_counts_by_cities)

print("City with lowest total precipitation:")
print(index_of_lowest_total_precipitation())

print("Average precipitation in each month:")
print(get_monthly_average_precipitation())

print("Average precipitation in each city:")
print(get_daily_average_precipitation())

