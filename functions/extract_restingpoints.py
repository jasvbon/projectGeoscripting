### This file contains functions 'haversine' and 'extractrestingpoints, which:
#   - calculate the distance between two sequenced datapoints;
#   - identifies resting points based on no movement;
#   - extracts these resting points to a new dataframe df_resting;
#   - masks datapoints that do not imply more than 1 meter movement;
#   - returns the masked dataframe and the dataframe containing resting points.


def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    import numpy as np

    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
    a = np.sin((lat2-lat1)/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2
    return earth_radius * 2 * np.arcsin(np.sqrt(a)) * 1000


def extractrestingpoints(df_lhist):
    import numpy as np

    # adding columns required for calculating the haversine distance
    df_lhist.insert(loc=len(df_lhist.columns), column='RestingPoint', value=None)
    df_lhist.insert(loc=len(df_lhist.columns), column='latshift', value=df_lhist['lat'].shift(1))
    df_lhist.insert(loc=len(df_lhist.columns), column='lonshift', value=df_lhist['lon'].shift(1))
    df_lhist = df_lhist.drop(df_lhist.index[0])
    df_lhist.insert(loc=len(df_lhist.columns), column='MovementMeter',
                    value=haversine(df_lhist['lat'], df_lhist['lon'],
                                    df_lhist['latshift'], df_lhist['lonshift'],
                                    to_radians=True, earth_radius=6373))

    # identifying resting points based on no movement taking place.
    df_lhist['RestingPoint'] = np.where(df_lhist['MovementMeter'] != 0, False, df_lhist['RestingPoint'])
    df_lhist['RestingPoint'] = np.where(df_lhist['MovementMeter'] == 0, True, df_lhist['RestingPoint'])

    # saving all resting points to new dataframe
    restingmask = df_lhist['RestingPoint'] == True
    df_resting = df_lhist.loc[restingmask]

    # applying a mask to remove points that signify less than 1 meter of movement
    premask_n_datapoints = len(df_lhist)
    mask = df_lhist['MovementMeter'] > 1
    df_lhist = df_lhist.loc[mask]

    # print function feedback to user
    n_datapoints = '{:,}'.format(premask_n_datapoints - len(df_lhist)).replace(',', ' ')
    statement = 'A total of {} datapoints did not incur movement; they were removed. \n'
    print(statement.format(n_datapoints))

    df_lhist = df_lhist.drop(columns=['RestingPoint', 'latshift', 'lonshift'])
    df_resting = df_resting.drop(columns=['MovementMeter', 'latshift', 'lonshift'])

    return df_lhist, df_resting
