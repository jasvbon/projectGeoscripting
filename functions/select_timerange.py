# This file contains function 'set_timeframe', which:
#   - drops all datapoint entries from the dataframe which fall outside of the requested timeframe;
#   - prints first and last found entries in dataset within timeframe and old and new n of datapoints;
#   - returns the dataframe of the selected timeframe.


def set_timeframe(df_lhist, start_date, end_date):
    import pandas as pd
    old_n_datapoints = '{:,}'.format(len(df_lhist)).replace(',',' ')

    # Converting the dataset ton a DatetimeIndex for daterange selection
    df_lhist['datetime'] = pd.to_datetime(df_lhist['datetime'])
    mask = (df_lhist['datetime'] >= start_date) & (df_lhist['datetime'] <= end_date)
    df_timeframe = df_lhist.loc[mask]
    n_datapoints = '{:,}'.format(len(df_lhist)).replace(',',' ')

    # Print a statement of the first and last entries within the timeframe, and old and new n of datapoints
    statement = 'The dataset now contains data from {} until {}, and has been reduced from {} to {} datapoints. \n'
    mindate = str(df_timeframe['datetime'].min())
    maxdate = str(df_timeframe['datetime'].max())
    if mindate[:10] == maxdate[:10]: # if the date is the same, it will print time interval instead of date interval
        print(statement.format(mindate, maxdate[11:], old_n_datapoints, n_datapoints))
    else:
        print(statement.format(mindate[:10], maxdate[:10], old_n_datapoints, n_datapoints))

    return df_timeframe
