### This file contains function 'importdata', which:
#   - takes latitude, longitude, time of recording and accuracy from the location history json;
#   - converts these attributes to appropriate format;
#   - returns a dataframe with these attributes.


def importdata(data_folder, filename):
    import pandas as pd
    from datetime import datetime as dt

    # assigning dataframe to input json file
    df_lhist = pd.read_json(data_folder+'/'+filename)
    df_lhist['lat'] = df_lhist['locations'].map(lambda x: x['latitudeE7'])
    df_lhist['lon'] = df_lhist['locations'].map(lambda x: x['longitudeE7'])
    df_lhist['timestamp_ms'] = df_lhist['locations'].map(lambda x: x['timestampMs'])
    df_lhist['accuracy'] = df_lhist['locations'].map(lambda x: x['accuracy'])
    # relevant data has been extracted, therefore the source can be deleted for optimisation purposes
    df_lhist = df_lhist.drop(columns='locations')

    # converting Latitude, Longitude to decimal degrees and timestamp to date-time format
    df_lhist['lat'] = df_lhist['lat'] / 10.**7
    df_lhist['lon'] = df_lhist['lon'] / 10.**7
    df_lhist['timestamp_ms'] = df_lhist['timestamp_ms'].astype(float) / 1000
    df_lhist['datetime'] = df_lhist['timestamp_ms'].map(lambda x: dt.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

    # removing all inaccurate datapoints with accuracy over 50
    n_premask = len(df_lhist)
    mask = df_lhist['accuracy'] < 50
    df_lhist = df_lhist.loc[mask]
    n_inaccurate = '{:,}'.format(n_premask - len(df_lhist)).replace(',', ' ')

    # printing results of function to user
    n_datapoints = '{:,}'.format(len(df_lhist)).replace(',', ' ')
    statement = 'Succesfully imported data from {} until {}, containing {} datapoints. \n' \
                'A total of {} inaccurate datapoints were removed upon importing. \n'
    print(statement.format(df_lhist['datetime'].min()[:10],
                           df_lhist['datetime'].max()[:10],
                           n_datapoints,
                           n_inaccurate))


    return df_lhist
