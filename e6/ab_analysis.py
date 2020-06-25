import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)

def chi_square_test_users(users):
    odd_uid_users = users[users['odd_uid'] == True]
    even_uid_users = users[users['odd_uid'] == False]
    odd_users_searched_atleast_once = len(odd_uid_users[odd_uid_users['search_count'] > 0].index)
    odd_users_never_searched = len(odd_uid_users[odd_uid_users['search_count'] == 0].index)
    even_users_searched_atleast_once = len(even_uid_users[even_uid_users['search_count'] > 0].index)
    even_users_never_searched = len(even_uid_users[even_uid_users['search_count'] == 0].index)
    contingency = [[even_users_searched_atleast_once, even_users_never_searched],
                   [odd_users_searched_atleast_once, odd_users_never_searched]]
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return p

def chi_square_test_instr(instr):
    odd_uid_instr = instr[instr['odd_uid'] == True]
    even_uid_instr = instr[instr['odd_uid'] == False]

    odd_instr_searched_atleast_once = len(odd_uid_instr[odd_uid_instr['search_count'] > 0].index)
    odd_instr_never_searched = len(odd_uid_instr[odd_uid_instr['search_count'] == 0].index)

    even_instr_searched_atleast_once = len(even_uid_instr[even_uid_instr['search_count'] > 0].index)
    even_instr_never_searched = len(even_uid_instr[even_uid_instr['search_count'] == 0].index)

    contingency = [[even_instr_searched_atleast_once, even_instr_never_searched],
                   [odd_instr_searched_atleast_once, odd_instr_never_searched]]

    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return p

def u_test_users(users):
    odd_uid_users = users[users['odd_uid'] == True]
    even_uid_users = users[users['odd_uid'] == False]
    return stats.mannwhitneyu(even_uid_users['search_count'].values, odd_uid_users['search_count'].values, alternative="two-sided").pvalue

def u_test_instr(instr):
    odd_uid_instr = instr[instr['odd_uid'] == True]
    even_uid_instr = instr[instr['odd_uid'] == False]
    return stats.mannwhitneyu(even_uid_instr['search_count'].values, odd_uid_instr['search_count'].values, alternative="two-sided").pvalue

def main():
    searchdata_file = sys.argv[1]
    data = pd.read_json(searchdata_file, orient='records', lines=True)
    data['odd_uid'] = data['uid'].apply(lambda x: x % 2 != 0)
    instr = data[data['is_instructor'] == True]
    more_users_p = chi_square_test_users(data)
    more_searches_p = u_test_users(data)
    more_instr_p = chi_square_test_instr(instr)
    more_instr_searches_p = u_test_instr(instr)
    
    

    # ...

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=more_users_p,
        more_searches_p=more_searches_p,
        more_instr_p=more_instr_p,
        more_instr_searches_p=more_instr_searches_p,
    ))


if __name__ == '__main__':
    main()
