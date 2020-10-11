# Run this app with `python3 app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import random

########## create the figure
fig = go.Figure()

# ***************** get plant image from databse
# hardcoded for now but will later be stored in the DB
import base64
with open("static/plant.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
#add the prefix that plotly will want when using the string as source
encoded_image = "data:image/png;base64," + encoded_string

########## configure the height and width
img_width = 1900
img_height = 1400
scale_factor = 0.7

# Configure axes
fig.update_xaxes(
    visible=True,
    range=[0, img_width * scale_factor]
)

fig.update_yaxes(
    visible=True,
    range=[0, img_height * scale_factor],
    # the scaleanchor attribute ensures that the aspect ratio stays constant
    scaleanchor="x"
)

# Add image
fig.add_layout_image(
    dict(
        x=0,
        sizex=img_width * scale_factor,
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source= encoded_image)
)

# Configure other layout
fig.update_layout(
    width=img_width * scale_factor,
    height=img_height * scale_factor,
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

# ***************** get location of stations from database
# hardcoded stations for now
# explore using the add_annotation feature to allow layout to be drawn by user
# the stations could be drawn and then updated in the DB for use

# dictionary of stations
# each station is drawn as a rectangle using the BL and TR coordinates
# format--> station#: [x0,x1,y0,y1]
stations = {1: [170, 470, 670, 860], 
            2: [170, 470, 470, 650],
			3: [480, 700, 470, 650],
            4: [710, 990, 470, 650],
            5: [1000, 1200, 470, 650],
            6: [170, 470, 290, 460],
            7: [480, 700, 290, 460],
            8: [710, 1200, 290, 460]
}
# ***************** get location of aircrafts
# aircrafts is a nested dictiorany
# the key is the tagID for that aircraft
# the nested dictionary contains information about that aircraft (model, )
aircrafts = {111: {"model": "Phenom", "ID": 47830, "x":700, "y":350}}

# add some random points for demo purposes
for i in range(5):
	new_ac = {"model": "Phenom", 
	         "ID":random.randint(1, 50000),
					 "x": random.randint(100, 1100),
					 "y": random.randint(320, 700) 
	}
	aircrafts[random.randint(1, 300)] = new_ac

# Creat shapes for stations and trace for ACs			
station_labels = []
station_centers_X = []
station_centers_Y = []
station_colors = ['darkgrey', 'lightgrey', 'lightslategrey', 'grey']
color_count = -1

# loop to display each station on the plant image
for num in stations.keys():
	color_count +=1
	# save the label and label positions
	# the position of the label will be the top center of the shape
	station_labels.append("Station #" + str(num))
	station_centers_X.append((stations[num][0]+stations[num][1])/2)
	station_centers_Y.append(stations[num][2]+20)

	# create a shape for the station
	fig.add_shape(
		type='rect',
		x0= stations[num][0], x1=stations[num][1], y0=stations[num][2], y1=stations[num][3],
		xref='x', yref='y',
		line_color='DarkBlue',
		fillcolor= station_colors[color_count%(len(station_colors))],
		opacity = 0.5
	)
 
# add the station labels as a trace
fig.add_trace(go.Scatter(
		x= station_centers_X,
		y= station_centers_Y,
		text= station_labels,
		textfont=dict(
        family="Arial",
        size=20,
        color="black"
    ),
		mode="text"
))

# loop to get x an y of each aircraft
# labels holds the information to be displayed for that aircraft
x_coord = []
y_coord = []
ac_labels = []
display_info = []
for ac in aircrafts:
	# check that both an x and y coordinate exist 
	if(aircrafts[ac]['x'] and aircrafts[ac]['y']):
		x_coord.append(aircrafts[ac]['x'])
		y_coord.append(aircrafts[ac]['y'])
		ac_labels.append('ID:' + str(aircrafts[ac]['ID']))
		display_info.append(aircrafts[ac]['model'] + '\n\nAdd desired information here')
		
# display points with ac_labels
fig.add_trace(
		go.Scatter(
				x=x_coord,
				y=y_coord,
				mode="markers+text",
				# markers are royal blue circles with a black outline
				marker=dict(
            color='RoyalBlue',
						symbol='triangle-right',
            size=50,
            line=dict(
                color='Black',
                width=2
            )
        ),
				text=ac_labels,
				hovertext=display_info,
				textposition='bottom center'
		)
	
)

# disable zooming feature on map
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True