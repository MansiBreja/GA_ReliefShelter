# GA_ReliefShelter

* my dataset folder has the initial data set collected from a government website. It contains information about the towns and villages in all the districts of Kerala.
* gascript.py is the python script to extract data from the csv files in the above stated folder and the number of days before submerging and cost have been generated randomly. The reason for random generation is that this data is dynamic and can only be available in case of an actual calamity at that place.
* Now the problem we faced was that geopy was returning empty geocodes for certain locations due to the server being unable to handle too many requests. So we added the latitude and longitude in the dataset file itself. The python script used for this was lat_lan_add_script.py
* The final dataset that is used as input in out GA code is in dataset2.csv (generated using the above stated python script)
* Our main GA code is in main.py
* Our final population's best chromosome is plotted on map and is stored in index.html
* Also, the GA code, after running completely plots a graph of average fitness over generations as shown below:


![screenshot 224](https://user-images.githubusercontent.com/31369977/47204564-47a52200-d3a1-11e8-86e2-10f70827082f.png)


## This is how index.html looks like:
![screenshot 223](https://user-images.githubusercontent.com/31369977/47204336-b9c93700-d3a0-11e8-94e6-e51fee0bc367.png)
