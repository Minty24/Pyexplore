#---- Assignment BokehSeverAssignment Code ----#

#Import gapminder csv file to python
import pandas as pd 
data=pd.read_csv('gapminder.csv',index_col='Year')

# Import the necessary modules
from bokeh.io import curdoc
from bokeh.io import output_file, show

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import Button

import bokeh.palettes
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6

from bokeh.layouts import row, widgetbox
from bokeh.models import Slider
from bokeh.models import HoverTool, Select
from bokeh.io import output_notebook, show


# - Set up the ColumnDataSource; Define the min and max for both x-axis(fertility) and y-axis(life)
source = ColumnDataSource(data={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country' : data.loc[1970].Country,
    'pop'     : (data.loc[1970].population / 20000000) + 2,
    'region'  : data.loc[1970].region,

})

xmin, xmax = min(data.fertility), max(data.fertility)

ymin, ymax = min(data.life), max(data.life)

# Create the plot figure and add circle glyphs to the figure
plot = figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
          x_range=(xmin, xmax), y_range=(ymin, ymax))

plot.circle(x='x', y='y', fill_alpha=0.8, source=source)

plot.xaxis.axis_label ='Fertility (children per woman)'

plot.yaxis.axis_label = 'Life Expectancy (years)'

#Make a list of the unique value from the region and display the legend to the bottom left  

regions_list = data.region.unique().tolist()

color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
        color=dict(field='region', transform=color_mapper), legend='region')

plot.legend.location = 'bottom_left'

#--- Creating the hover for graph ---#

hover = HoverTool(tooltips=[('Country', '@country')])

plot.add_tools(hover)

#--- Creating Slider and Drop down meau for graph ---#

# Define the callback: update_plot
def update_plot(attr, old, new):
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y

    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }

    source.data = new_data

    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

#Title
    plot.title.text = 'Gapminder data for %d' % yr

# Create a dropdown slider widget: slider, and attach the callback to the 'value' property of slider
slider = Slider(start=1964, end=2013, step=1, value=1970, title='Year from 1964 - 2013')

slider.on_change('value', update_plot)

# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='X-axis Choices'
)

x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='Y-axis Choices'
)

y_select.on_change('value', update_plot)

# Create layout and display the gragh
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)

#End --- 