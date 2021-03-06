# import the necessary python libraries
import numpy as np
import csv
import matplotlib
matplotlib.use("Agg")
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# open a new figure
fig = plt.figure(figsize=(12,8))

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

# get lat and lon for label
xpt,ypt = m(-55.0,30.0)

# save the figure
plt.text(xpt,ypt,'No active storms',ha='center',size='large')
plt.savefig('/var/www/html/images/tracking_chart.png', orientation='landscape', bbox_inches='tight')
print('Great success!')
