# GA_ReliefShelter
A terminal based app which selects the most optimal ‘p’ locations for constructing relief shelters in the time of floods, using a genetic algorithm based on features like latitude, longitude, population and expected number of days to submerge. It takes into consideration conflicting objectives like maximisation of a quantity known as population score and minimising the average distance to any shelter, while making sure the cost does not exceed the total budget.

## Constraints:

* Budget= B crores
* Population finally accumulated <= K  * (current population)
* submerged_days(x) >= max( submerged_days(y) for all y)
* submerged_days(x)>0

## Objectives:

* O1 Maximize the population score i.e an indicator of the number of people saved
* O2 Minimise the average distance to any relief shelter.
* O3 Maximize the cost within the budget.

## Objective Function/Fitness function:
F= (O1 + O3 )/O2

## Implementation
* my dataset folder has the initial data set collected from a government website. It contains information about the towns and villages in all the districts of Kerala.
* gascript.py is the python script to extract data from the csv files in the above stated folder and the number of days before submerging and cost have been generated randomly. The reason for random generation is that this data is dynamic and can only be available in case of an actual calamity at that place.
* Now the problem we faced was that geopy was returning empty geocodes for certain locations due to the server being unable to handle too many requests. So we added the latitude and longitude in the dataset file itself. The python script used for this was lat_lan_add_script.py
* The final dataset that is used as input in out GA code is in dataset2.csv (generated using the above stated python script)
* Our main GA code is in main.py
* Our final population's best chromosome is plotted on map and is stored in index.html
* Also, the GA code, after running completely plots a graph of average fitness over generations as shown below:

![graph](https://user-images.githubusercontent.com/31369977/47575320-77cf6080-d95f-11e8-8979-7bf4a6a859ee.png)


## This is how index.html looks like:
![screenshot 223](https://user-images.githubusercontent.com/31369977/47204336-b9c93700-d3a0-11e8-94e6-e51fee0bc367.png)

This project was collectively made by [Sanchit Aggarwal](https://github.com/mr-logix) and [Mansi Breja](https://github.com/MansiBreja) as a part of a 5th Semester course on Genetic Algorithms, NSIT. 
