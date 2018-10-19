# GA_ReliefShelter

* my dataset folder has the initial data set collected from a government website. It contains information about the towns and villages in all the districts of Kerala.
* gascript.py is the python script to extract data from the csv files in the above stated folder and the number of days before submerging and cost have been generated randomly. The reason for random generation is that this data is dynamic and can only be available in case of an actual calamity at that place.
* Now the problem we faced was that geopy was returning empty geocodes for certain locations due to the server being unable to handle too many requests. So we added the latitude and longitude in the dataset file itself. The python script used for this was lat_lan_add_script.py
* The final dataset that is used as input in out GA code is in dataset2.csv (generated using the above stated python script)
* Our main GA code is in main.py
