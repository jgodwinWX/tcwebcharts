# import the necessary python libraries
import matplotlib
matplotlib.use('Agg')
import numpy as np
import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

################ User controls #######################

atcf_file = ['/home/jgodwin/python/web_tracking_chart/bal962019.csv']
# if namedStorm is set to True, the invest portion of the track will be ommitted
namedStorm = [False]

######################################################

storm_date = []
storm_lat = []
storm_lon = []
storm_wind = []
storm_pressure = []
storm_type = []
storm_name = []
storm_color = []

for f in range(len(atcf_file)):
	############### Section 1: importing the data ########
	# open the CSV file
	print('Opening file')
	atcf_data = open(atcf_file[f],'r')
	reader = csv.reader(atcf_data,delimiter=',')

	# set up the variables for the data we wish to import
	date = []
	lat = []
	lon = []
	wind = []
	pressure = []
	tc_type = []
	tc_name = []

	# make sure all rows are the same length then import the data
	print('Importing data')
	for row in reader:
		row += [None] * (35 - len(row))
       		date.append(row[2])
		lat.append(row[6])
		lon.append(row[7])
		wind.append(float(row[8]))
		pressure.append(float(row[9]))
		tc_type.append(row[10])
		tc_name.append(row[27])

	# re-format the latitude, longitude, and tc_type data
	for x in range(len(lat)):
		if lat[x][-1] == 'N':
			lat[x] = float(lat[x][:-1]) / 10.0
		else:
			lat[x] = -1.0 * (float(lat[x][:-1]) / 10.0)
		if lon[x][-1] == 'E':
			lon[x] = float(lon[x][:-1]) / 10.0
		else:
			lon[x] = -1.0 * (float(lon[x][:-1]) / 10.0)
			tc_type[x] = tc_type[x][1:]

		if tc_name[x] != None:
			tc_name[x] = tc_name[x].strip()

	############### Section 2: drawing the map ###########
	# open a new figure
	fig = plt.figure(figsize=(10,8))

	# draw the map
	print('Drawing map')
	m = Basemap(projection='merc', llcrnrlat=5.0, urcrnrlat=50.0, llcrnrlon=-105.0, urcrnrlon=-10.0, resolution='i', lat_ts=20.0)
	m.drawlsmask(land_color='coral', ocean_color='aqua', lakes='False')

	# draw parallels and meridians
	m.drawparallels(np.arange(5.0, 50.0, 10.0), linewidth=1, dashes=[1,1], labels=[True, True, False, False], color='gray')
	m.drawmeridians(np.arange(-105.0, 10.0, 10.0), linewidth=1, dashes=[1,1], labels=[False, False, True, True], color='gray')

	# draw boundaries
	m.drawmapboundary(fill_color='white')
	m.drawstates(color='gray',linewidth=1)
	m.drawcountries(color='black',linewidth=2)
	m.drawcoastlines()

	############### Section 3: plotting the data #########
	# set intensity colours
	tc_color = []
	for j in range(len(tc_type)):
		if tc_type[j] == 'WV' or tc_type[j] == 'LO' or tc_type[j] == 'DB':
                        if namedStorm[f]:
                            tc_color.append('skip')
                        else:
			    tc_color.append('ko')
		elif tc_type[j] == 'TD' or tc_type[j] == 'SD':
			tc_color.append('bo')
		elif tc_type[j] == 'TS' or tc_type[j] == 'SS':
			tc_color.append('go')
		elif tc_type[j] == 'HU' and wind[j] <= 95:
			tc_color.append('ro')
		elif tc_type[j] == 'HU' and wind[j] > 95:
			tc_color.append('mo')

	storm_date.append(date)
	storm_lat.append(lat)
	storm_lon.append(lon)
	storm_wind.append(wind)
	storm_pressure.append(pressure)
	storm_type.append(tc_type)
	storm_color.append(tc_color)
	storm_name.append(tc_name)

# plot the tracks
print('Plotting storm')
for s in range(len(atcf_file)):
	for i in range(len(storm_date[s])):
        		alon, alat = storm_lon[s][i], storm_lat[s][i]
       			xpt, ypt = m(alon, alat)
 	       		lonpt, latpt = m(xpt, ypt, inverse=True)
                        if storm_color[s][i] == 'skip':
                            continue
                        else:
       			    m.plot(xpt, ypt, storm_color[s][i])
			    if i == len(storm_date[s])-1:
				    plt.text(xpt+0.3, ypt+0.3, storm_name[s][i], fontsize=10, color='black')

# save the figure
plt.savefig('/home/jgodwin/python/web_tracking_chart/tracking_chart.png', orientation='landscape', bbox_inches='tight')
print('Great success!')
