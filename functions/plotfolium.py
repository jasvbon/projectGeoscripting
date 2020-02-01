def plotfolium(df):
    import matplotlib.pyplot as plt
    from datetime import datetime
    import contextily as ctx
    import geopandas as gpd
    from shapely.geometry import Point
    from shapely.geometry import LineString
    import pandas as pd
    import numpy as np
    import folium
    import branca

    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df["time"] = df.index
    df["time"] = pd.to_datetime(df['time'])

    # make a points df for each day
    points_df = df.resample('D',label='right').first()

    # make df into gdf
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    points_geometry = [Point(xy) for xy in zip(points_df.lon, points_df.lat)]

    df = df.drop(['lon', 'lat'], axis=1)
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:4326'}, geometry=geometry)

    points_gdf = gpd.GeoDataFrame(points_df, crs={'init': 'epsg:4326'}, geometry=points_geometry)

    # ctx requires web mercator
    crs = {'init': 'epsg:3857'}
    gdf  = gdf.to_crs(crs)
    points_gdf = points_gdf.to_crs(crs)
    points_gdf = points_gdf.reset_index()

    # Prepare aggregation for GroupBy
    gdf['lines_id'] = gdf['time'].dt.date

    # Mask away all dates containing less than 1 datapoints because it is not possible to make a line from them
    gdf.insert(loc=len(gdf.columns), column='freq', value=gdf['lines_id'].map(gdf['lines_id'].value_counts()))
    freqmask = gdf['freq'] > 2
    gdf = gdf.loc[freqmask]

    # Aggregate with GroupBy
    lines_gdf = gdf.groupby(['lines_id'])['geometry'].apply(lambda x: LineString(x.tolist()))
    lines_gdf = gpd.GeoDataFrame(lines_gdf, geometry='geometry')
    lines_gdf.crs = crs
    lines_gdf = lines_gdf.reset_index()

    # Make strings out of the datetime, for the foliumplot, datetime objects confuse it
    points_gdf["datetime"] = points_gdf["datetime"].astype(str)
    points_gdf["Timestamp"] = points_gdf["datetime"].astype(str)
    points_gdf["time"] = points_gdf["time"].astype(str)
    lines_gdf["lines_id"] = lines_gdf["lines_id"].astype(str)

    startTime = points_gdf["time"].iloc[0]
    endTime = points_gdf["time"].iloc[-1]

    # initialize plot
    f, ax = plt.subplots()

    points_gdf.plot(ax=ax)
    lines_gdf.plot(ax=ax, cmap="plasma")

    # Labeling
    ax.set_xlabel('Web Mercator Longitude')
    ax.set_ylabel('Web Mercator Latitude')

    # Create numpy-array images a,c and boundings boxes b,d with terrain lines and background using Contextily
    ctx.add_basemap(ax, url=ctx.tile_providers.ST_WATERCOLOR)
    ax.set_axis_off()
    plt.legend(["Day starting point", "Movement Path"], loc = "lower left",bbox_to_anchor=(0.5, 0, 0.5, 0.5))

    plt.title('Visualized Google Location Path', fontsize=14, fontweight='bold')
    plt.show()
    plt.savefig("./output/Location History from " + startTime+ " : " + endTime+".png")
    print("saved plot image in: "+"./output/Location History from " + startTime+ " : " + endTime+".png")

    # get it ready for the folium colormap, as the oid will be the colors that are plotted
    p = lines_gdf.groupby('lines_id').grouper.group_info[0] + 1
    lines_gdf["oid"] = p
    variable = 'oid'


    # make the colormap
    colorscale = branca.colormap.linear.Set1_04.scale(lines_gdf[variable].min(), lines_gdf[variable].max())
    colorscale = colorscale.to_step(n=len(lines_gdf[variable]), quantiles=lines_gdf[variable])  ## sets quantile breaks
    colorscale.caption = "Days for movements in location history"  ## adds name for legend

    # initiate colormap
    m = folium.Map(tiles="Stamen Watercolor")

    # plot the lines
    folium.GeoJson(lines_gdf,
                   style_function=lambda x: {'color': colorscale(x['properties'][variable]), 'weight': 4}).add_to(m)
    # plot the points
    folium.GeoJson(points_gdf, tooltip=folium.features.GeoJsonTooltip(fields=['Timestamp'], localize=True)).add_to(m)
    # add the colormap
    colorscale.add_to(m)

    m.fit_bounds(m.get_bounds())
    m.save("./output/Location History from " + startTime+ " : " + endTime+".html")
    print("saved folium in: "+"./output/Location History from " + startTime+ " : " + endTime+".html")