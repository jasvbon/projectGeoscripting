def threedplot (df):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from datetime import datetime
    import contextily as ctx
    import geopandas as gpd
    from shapely.geometry import Point
    import pandas as pd
    import numpy as np

    # conversion of crs from df to gdf
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    df = df.drop(['lon', 'lat'], axis=1)
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:4326'}, geometry=geometry)

    # ctx requires web mercator
    crs = {'init': 'epsg:3857'}
    gdf = gdf.to_crs(crs)

    # extract lat lon points from the gdf to be able to plot the 3D in matplotlib
    X = []
    Y = []
    for index, row in gdf.iterrows():
        for pt in list(row['geometry'].coords):
            x, y = pt
            X.append(x)
            Y.append(y)

    # format dates to integers for Z-axis
    dates_formatted = [pd.to_datetime(d) for d in gdf["datetime"]]
    time = [(d - min(dates_formatted)).seconds * 100000 for d in dates_formatted]

    # initialize plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plt.suptitle('Space Time Cube', fontsize=14, fontweight='bold')

    # Set title with timecodes of location data
    startTime = gdf["datetime"].iloc[0]
    endTime = gdf["datetime"].iloc[-1]
    plt.title('From {} to {}'.format(startTime, endTime))

    # Labeling
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Seconds')

    # Plot the path over space and time
    ax.plot(X, Y, time, zorder=100)

    # Get min and max bounding box from the plot
    xmin, xmax, ymin, ymax = ax.axis()

    # Create numpy-array images a,c and boundings boxes b,d with terrain lines and background using Contextily
    a, b = ctx.bounds2img(xmin, ymin, xmax, ymax, url=ctx.tile_providers.ST_TERRAIN)

    # Make a meshgrid from the bounding box and place the numpy raster in it, which is a three band raster
    x = np.linspace(xmin, xmax, a.shape[1])
    y = np.linspace(ymin, ymax, a.shape[0])
    xx, yy = np.meshgrid(x, y, indexing="xy")

    # Convert this raster image to a grayscale version of itself
    roads = np.dot(a[...,:3], [0.299, 0.587, 0.144])

    # Plot the contours of grayscale images, imshow does not work in 3d plots
    ax.contourf(xx, yy, roads, levels=10, cmap="gist_gray", zorder=0)
    plt.savefig("./output/3D Space-time plot"+".png")
    print("saved plot image in the output folder as 3D Space-time plot.png")

    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(0.01)
