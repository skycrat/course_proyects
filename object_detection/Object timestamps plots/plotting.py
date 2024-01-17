from main import df 
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H: %M: %S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H: %M: %S")

#this prevent the problem of fetching the data from the dataframe
cds = ColumnDataSource(df)

p = figure(x_axis_type = "datetime" , height = 300, width = 900, title = "Motion Graph")
#p.yaxis.minor_tick_line_color = None

hover = HoverTool(tooltips = [("Start: " , "@Start_string"), ("End: ", "@End_string")])
p.add_tools(hover)

#bottom is 0 and top is 1 because they are fixed values
q = p.quad(source = cds, left = "Start", right = "End", bottom = 0, top= 1, color = 'green')


output_file(".venv\Data Visualization with Bokeh\Graph.html")
show(p)
