# Geoscripting project repository. 

Geoscripting 2020 
- Title: Location History Visualiser
- Team: Gothic Concrete Tractors
- Date: 21-01-20

prerequisites:
contextily for the basemap
when your enviroment is activated with source active envname
conda install contextily --channel conda-forge



Task 1: Why? short description of what you want to do

    The Google location history is a tracker that follows the location of your phone. If this feature is enabled, this data is available for download from Google.
    Using this location history, we will make a script that can automatically visualize this data in a 3D map, where time is on the Z axis. This can be a cool way tovisualize a vacation, small city trip or perhaps all data available. The input will be the dataset and the dates you want to visualize

Task 2: What? Describe data set
    The dataset is a JSON object, of all the locations you have been. Usually at a 12s temporal resolution.
    This can be downloaded at https://takeout.google.com/
    One of the cases is our personal dataset, of which a complete dataset of 3 years is around 13MB. It is filled of X/Y coordinates, direction and modality.
    
Task 3: How?: Methods and potential results
    The first step is to extract the data and convert it to points, following this step, we want to build a 3d polyline out of it, with time on the Z-axis. 
    This data can be visualized using MatplotLib 3D in Python, with a useful basemap. The result of this, is a movable 3d map of the locations you where on your journey.
    This script can be used by anyone, so they can also visualize their results.
    The reproducibility of this script is key, as we want it to have functionality to enter a range of dates, of any location, of any person. This way we can in the future also make actual personal use of it, instead of making a script we will never use again.

    More functionality?
    
4. Create a pull request by following the descripting in the following explanation strictly 

6. Then review another team
