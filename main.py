####    Geoscripting Project
###     Team Gothic Concrete Tractors
##      Jasper van Bon - Jurrian Doornbos
#       27-31 January 2020



###

# We have personal datasets spanning 3+ years, but for privacy's sake we only give users 1 week of location history.
# A dataset of 1 week of traveling in New Zealand has been included for demonstration purposes.
# The timeframe of this dataset is from '2018-11-11 00:00:00' to '2018-11-18 23:59:59'.

# User: define your inputs! (current settings are default, to showcase the working project)
data_folder = './data'
lhist_filename = 'LH_1weekofNZ.json' # total dataset could be imported as: lhist_filename = 'Location History.json'

# If custom timeframe is desired, set False to True, and enter timeframe in this datetime format.
# For demonstration purposes, after viewing the entire dataset, user can set to true to view 2 days out of all 8 days.
# Note that timeframe is re-runable and the data import function does not need to be run when changing timeframe.
# Note that due to limitations in zoomlevel of backgroundmap, viewing single days in the 2dplot likely runs into error.
customtimeframe  = False
start_date = '2018-11-13 00:00:00'
end_date = '2018-11-16 23:59:59'

# 3D plot is a very heavy plugin to run, highly recommended to only plot it if your timeframe is of a single day.
# This plot may take a minute or two to load. Be aware and be patient.
give3dplot = False

###



# importing functions
from functions.import_and_preprocess import importdata
from functions.select_timerange import set_timeframe
from functions.threedplot import threedplot
from functions.plotfolium import plotfolium
from functions.extract_restingpoints import extractrestingpoints
import os.path


# Checking for valid folder and filename.
if not os.path.exists('output'): os.mkdir('output')
if os.path.exists(data_folder) == False: raise Exception('Sorry, but the input datafolder:', data_folder, ' does not exist.')
if os.path.isfile(data_folder + '/' + lhist_filename) == False: raise Exception('Sorry, but the input filename:', lhist_filename, 'can not be found in the directory:', data_folder)


# importing data to pandas dataframe
df_lhist = importdata(data_folder, lhist_filename)


# if custom timeframe is set to true, data is masked to given timeframe. Else, all datapoints are taken.
if customtimeframe: df_timeframe = set_timeframe(df_lhist, start_date, end_date)
else: df_timeframe = df_lhist


# extracting stillstanding datapoints for data optimisation
df_timeframe, df_resting = extractrestingpoints(df_timeframe)


# Plot a 2d folium html map, and a matplot that is exported into output folder as png
plotfolium(df_timeframe)
# Plot a 3d space time cube, and export it into output folder as png
if give3dplot: threedplot(df_timeframe)