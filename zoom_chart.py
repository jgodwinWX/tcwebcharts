import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas
import re

from datetime import datetime
from mpl_toolkits.basemap import Basemap

# function for creating the wind radii arcs
def arc_patch(center, radius, theta1, theta2, ax=None, resolution=50, **kwargs):
    # make sure ax is not empty
    if ax is None:
        ax = plt.gca()
    # generate the points
    w = mpatches.Wedge(center,radius,theta1,theta2,**kwargs)
    ax.add_artist(w)
    return w

# function for rounding the wind to the nearest multiple of five
def windRound(x):
    return int(5 * round(float(x)/5))

# user settings
atcf_file = '/home/jgodwin/python/web_tracking_chart/bal022019.csv'
stormname = 'Tropical Storm Barry'
test_mode = False

# conversion factors (constants)
NM_TO_M = 1852.0    # nautical miles to meters conversion factor
KT_TO_MPH = 1.15078 # knots to mph conversion factor

# column names for the ATCF best-track files
colnames = ['Basin','CY','Date/Time','Technum','Tech','Tau','Lat','Lon','Vmax','MSLP','Type','RadType',\
    'Quadrant','Rad1','Rad2','Rad3','Rad4','MaxP','MaxP Radius','Rmax','Gust','Eye','Subregion',\
    'MaxSeas','Fcstr','Direction','Speed','StormName','Depth','Seas','Seas Code','Seas1','Seas2',\
    'Seas3','Seas4','Remarks1','Remarks2','Remarks3','Remarks4','Remarks5']
# import the ATCF CSV into a pandas dataframe
atcf_data = pandas.read_csv(atcf_file,error_bad_lines=False,names=colnames)

# get the valid date and time, and prettify into a readable string for the plot title
valid = str(atcf_data.loc[atcf_data['Date/Time'].idxmax()]['Date/Time'])
dt = datetime.strptime(valid,'%Y%m%d%H')
dt_str = datetime.strftime(dt,'%m/%d/%Y %H')
# separate out the rows we actually want
vatcf = atcf_data[atcf_data['Date/Time'].astype(str).str.contains(valid)]
# latitude
latitude = float(re.findall(r'\d+',vatcf['Lat'].iloc[0])[0])/10.0
# longitude
longitude = -float(re.findall(r'\d+',vatcf['Lon'].iloc[0])[0])/10.0
# maximum sustained winds (kt) and minimum pressure (hPa)
vmax = float(vatcf['Vmax'].iloc[0])
mslp = float(vatcf['MSLP'].iloc[0])
# wind radii (nautical miles)
radtype = vatcf['RadType']
rad1 = vatcf['Rad1']
rad2 = vatcf['Rad2']
rad3 = vatcf['Rad3']
rad4 = vatcf['Rad4']

# set up basemap
fig = plt.figure(figsize=(10,8))
m = Basemap(projection='merc',llcrnrlat=latitude-5.0,urcrnrlat=latitude+5.0,\
    llcrnrlon=longitude-7.5,urcrnrlon=longitude+7.5,resolution='i',lat_ts=20.0)
m.bluemarble()
m.drawcounties(color='gray',linewidth=1)
m.drawstates(color='gray',linewidth=2)
m.drawcountries(color='black',linewidth=3)
m.drawcoastlines()
m.drawparallels(np.arange(0,90,2),labels=[True,False,False,False],color='white')
m.drawmeridians(np.arange(-180,180,2),labels=[False,False,False,True],color='white')

# plot the TC center
xpt,ypt = m(longitude,latitude)
m.plot(xpt,ypt,'ro',markersize=10)
# override the radii for test mode
if test_mode:
    radtype=pandas.Series([34,50,64])
    rad1=pandas.Series([150,75,30])
    rad2=pandas.Series([100,50,25])
    rad3=pandas.Series([25,10,5])
    rad4=pandas.Series([50,25,10])
# loop through all the wind radii
for ix,r in enumerate(radtype.values):
    # set the kwargs for the different wind radii
    if r == 34:
        radcolor = 'yellow'
    elif r == 50:
        radcolor = 'orange'
    elif r == 64:
        radcolor = 'magenta'
    else:
        radcolor = 'yellow'
    # create the wind radii arcs
    arc_patch((xpt,ypt),rad1.iloc[ix]*NM_TO_M,0,90,fill=True,color=radcolor,alpha=0.5)
    arc_patch((xpt,ypt),rad2.iloc[ix]*NM_TO_M,270,360,fill=True,color=radcolor,alpha=0.5)
    arc_patch((xpt,ypt),rad3.iloc[ix]*NM_TO_M,180,270,fill=True,color=radcolor,alpha=0.5)
    arc_patch((xpt,ypt),rad4.iloc[ix]*NM_TO_M,90,180,fill=True,color=radcolor,alpha=0.5)
# write current storm info
plt.annotate('Max Winds: %.0f mph\nMin Pressure: %.0f mb' % (windRound(vmax*KT_TO_MPH),mslp),(0,0),\
    (0,-20),xycoords='axes fraction',textcoords='offset points',va='top',fontsize=10)
plt.annotate('Latitude: %.1f\nLongitude: %.1f' % (latitude,longitude),(0,0),(150,-20),\
    xycoords='axes fraction',textcoords='offset points',va='top',fontsize=10)
# save figure
plt.title('%s - valid %s00 UTC' % (stormname,dt_str))
plt.savefig('/var/www/html/images/02L.png',bbox_inches='tight')
