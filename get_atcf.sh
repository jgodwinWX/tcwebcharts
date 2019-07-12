#!/bin/bash
# put the best-track ATCF files here
export DISPLAY=":0.0"
export CHART_PATH=/home/jgodwin/python/web_tracking_chart
wget http://hurricanes.ral.ucar.edu/realtime/plots/northatlantic/2019/al022019/bal022019.dat -O $CHART_PATH/bal022019.csv

# run the python script
python $CHART_PATH/web_chart.py >& $CHART_PATH/web_chart.log
python $CHART_PATH/zoom_chart.py >& $CHART_PATH/chart_zoomed.log

# send to website
cp $CHART_PATH/tracking_chart.png /var/www/html/images/.
