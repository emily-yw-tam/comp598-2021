"""
http://3.15.12.55:8080/nyc_dash?username=nyc&password=iheartnyc
"""

from bokeh.layouts import column, row
from bokeh.plotting import curdoc, figure
from bokeh.models import ColumnDataSource, Dropdown, Legend, LegendItem
import json

# authenticate any user who logs in with URL parameters username=nyc and password=iheartnyc
# failed authentications just need to fail to allow the user in
def authenticate_user(curdoc):
    args = curdoc.session_context.request.arguments
    
    username = args.get('username')[0].decode('utf-8')
    password = args.get('password')[0].decode('utf-8')

    if username != 'nyc':
        raise Exception('Incorrect username or password.')
    
    if password != 'iheartnyc':
        raise Exception('Incorrect username or password.')

def load_data():
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    all_data = data['all_data']
    zipcode_data = data['zipcode_data']
    zipcodes = data['zipcodes']

    return all_data, zipcode_data, zipcodes

def update_dropdown1(event):
    og = source.data['y_values'][2]
    source.data['y_values'] = [all_data, zipcode_data[event.item], og]

    p.y_range.start = 0
    p.y_range.end = max(max(all_data), max(zipcode_data[event.item]), max(og))

    print(f"HI {event.item} {type(event.item)} cri")

def update_dropdown2(event):
    og = source.data['y_values'][1]
    source.data['y_values'] = [all_data, og, zipcode_data[event.item]]

    p.y_range.start = 0
    p.y_range.end = max(max(all_data), max(og), max(zipcode_data[event.item]))

# authenticate user
c = curdoc()
authenticate_user(c)

# load data
loaded_data = load_data()
all_data = loaded_data[0]
zipcode_data = loaded_data[1]
zipcodes = loaded_data[2]
months = [1,2,3,4,5,6,7,8,9,10,11,12]
zeroes = [0,0,0,0,0,0,0,0,0,0,0,0]

# choose colours
red = 'red'
green = 'limegreen'
blue = 'dodgerblue'

# create plot
p = figure(x_range=(0,12), y_range=(0,170), x_axis_label='Month', y_axis_label='Average Response Time (Hours)', toolbar_location=None, title='Difference in response time to complaints filed through the 311 service by zipcode')
source = ColumnDataSource({'x_values':[months, months, months], 'y_values':[all_data, zeroes, zeroes], 'colours':[red, green, blue], 'legend':['All 2020 data', 'Zipcode 1', 'Zipcode 2']})

# line plot of monthly average response time for ALL 2020 data
p.multi_line(xs='x_values', ys='y_values', line_color='colours', line_width=2, legend_group='legend', source=source)

print(f'hello {type(zipcodes)}')

# dropdown for selecting zipcode 1
d1 = Dropdown(label='Zipcode 1', background=green, button_type='success', menu=zipcodes)
d1.on_click(update_dropdown1)

# dropdown for selecting zipcode 2
d2 = Dropdown(label='Zipcode 2', background=blue, button_type='primary', menu=zipcodes)
d2.on_click(update_dropdown2)

# put the button and plot in a layout and add to the document
c.add_root(column(p, d1, d2))

