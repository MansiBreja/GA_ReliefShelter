import os
import glob
import geopy.geocoders
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="GA")
from geopy.exc import GeocoderTimedOut
from geopy import distance
geopy.geocoders.options.default_timeout = 40
import csv
import random
with open ('/home/mansi/Desktop/GA/outputs/demo_output_bada.csv', mode='a') as ofile:
	data_writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for filepath in glob.glob(os.path.join('/home/mansi/Desktop/GA/my dataset','*.csv')):
		with open(filepath) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count<50:
					if list({row[10]})[0] in ['Rural']: 
						var=geolocator.geocode(list({row[9]})[0])
						if var is not None:	
							data_writer.writerow([list({row[9]})[0],list({row[12]})[0],random.randint(1,20), round(random.uniform(0, 15), 1), var, var.latitude, var.longitude])					
							line_count+=1
		
		

		
		
