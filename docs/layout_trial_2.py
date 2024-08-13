from bokeh.plotting import figure, show
import lasio

from lasview.depthwise import Layout

layout = Layout(4,3,width=(100,250),height=(50,50))

# depths = [100, 200, 300, 400, 500]  # Depths in reverse order
# curve1 = [0.1, 0.2, 0.3, 0.4, 0.5]  # Curve values for trail 1
# curve2 = [0.2, 0.3, 0.4, 0.5, 0.6]  # Curve values for trail 2

# source = ColumnDataSource(data=dict(depths=depths,curve1=curve1,curve2=curve2,))

file = lasio.read('digitized_data.las')

layout.set_depth(flip=True)
layout.set_label(cycle=3)

print(layout.trails)



# show(grid)