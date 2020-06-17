import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
pd.options.mode.chained_assignment = None  # default='warn'

OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)


def isInCanSubred2012Or2013(row):
    return row['date'].year in [2012, 2013] and row['subreddit'].lower() == 'canada'

def isWeekend(row):
    return row['date'].weekday() in [5,6]

def isWeekday(row):
    return not isWeekend(row)

def filterAndTransform(df):
    filtered = df.apply(isInCanSubred2012Or2013, axis=1)
    reddit_df = df[filtered]

    reddit_df['year'] = reddit_df.apply(lambda r: r['date'].isocalendar()[0], axis=1)
    reddit_df['week'] = reddit_df.apply(lambda r: r['date'].isocalendar()[1], axis=1)
    weekdays_df = reddit_df[reddit_df.apply(isWeekday, axis=1)]
    weekends_df = reddit_df[reddit_df.apply(isWeekend, axis=1)]
    
    return reddit_df, weekends_df, weekdays_df

def main():
    df  = pd.read_json(sys.argv[1], lines=True)
    reddit_df, weekends_df, weekdays_df = filterAndTransform(df)
    weekend_counts = weekends_df['comment_count']
    weekday_counts = weekdays_df['comment_count']

    plt.hist(weekday_counts)
    plt.show()
    # T-test, normality test and variance test
    ttest = stats.ttest_ind(weekend_counts, weekday_counts)
    initial_ttest_p = ttest.pvalue
    initial_weekday_normality_p = stats.normaltest(weekday_counts).pvalue
    initial_weekend_normality_p = stats.normaltest(weekend_counts).pvalue
    initial_levene_p = stats.levene(weekday_counts, weekend_counts).pvalue

    #Fix 1
    transformed_weekday_counts = np.sqrt(weekday_counts)
    transformed_weekday_normality_p = stats.normaltest(transformed_weekday_counts).pvalue
    transformed_weekend_counts = np.sqrt(weekend_counts)
    transformed_weekend_normality_p = stats.normaltest(transformed_weekend_counts).pvalue
    transformed_levene_p = stats.levene(transformed_weekend_counts, transformed_weekday_counts).pvalue

    #Fix 2
    weekly_weekday_counts = weekdays_df.groupby(['year','week']).mean()['comment_count']
    weekly_weekday_normality_p = stats.normaltest(weekly_weekday_counts).pvalue
    weekly_weekend_counts = weekends_df.groupby(['year','week']).mean()['comment_count']
    weekly_weekend_normality_p = stats.normaltest(weekly_weekend_counts).pvalue
    weekly_levene_p = stats.levene(weekly_weekday_counts, weekly_weekend_counts).pvalue
    weekly_ttest_p = stats.ttest_ind(weekly_weekday_counts, weekly_weekend_counts).pvalue
    utest_p = stats.mannwhitneyu(weekday_counts, weekend_counts).pvalue
    # ...
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=initial_ttest_p,
        initial_weekday_normality_p=initial_weekday_normality_p,
        initial_weekend_normality_p=initial_weekend_normality_p,
        initial_levene_p=initial_levene_p,
        transformed_weekday_normality_p=transformed_weekday_normality_p,
        transformed_weekend_normality_p=transformed_weekend_normality_p,
        transformed_levene_p=transformed_levene_p,
        weekly_weekday_normality_p=weekly_weekday_normality_p,
        weekly_weekend_normality_p=weekly_weekend_normality_p,
        weekly_levene_p=weekly_levene_p,
        weekly_ttest_p=weekly_ttest_p,
        utest_p=utest_p,
    ))


if __name__ == '__main__':
    main()
