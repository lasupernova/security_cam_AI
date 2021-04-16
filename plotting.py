# import motion data df
from motion import df

# import library
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

# add string-version of datetimes
df["Start_string"] = df['Start'].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df['End'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['Duration_string'] = str(df['Duration'])

# initiate ColumnDataSource object to easily pass data from source (here: df) to bokeh
cds = ColumnDataSource(df)

# initiate library with desired properties
f = figure(x_axis_type="datetime", height=100, width=500, sizing_mode="stretch_both", title="Big brother is watching!")

# modify y-axis
f.yaxis.minor_tick_line_color=None
f.yaxis.ticker.desired_num_ticks = 1

# create hover object; NOTE: hovertool ois not able to retrieve datetime objects --> convert to string before
hover = HoverTool(tooltips=[("Start","@Start_string"),("End", "@End_string")])
# add to figure object
f.add_tools(hover)

# plot times with motion as quadrants objects and add them to figure object
q = f.quad(left='Start', right='End', bottom=0, top=1, color='red', source=cds) #when source is given, df from which columns are takendo not need vto be specified

# define output file
output_file("Motion_detection.html")

show(f)