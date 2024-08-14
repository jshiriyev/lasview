from bokeh.plotting import show

from bokeh.layouts import gridplot

import lasio

from lasview import depthwise as dw

file = lasio.read('digitized_data.las')

layout = dw.Layout(4,
	ncurves = 3,
	depth = dict(values=file['DEPT'],spot=1),
	width = (100,250),
	height = (50,50),
	)

# print(layout.depth.spot)
# print(layout.depth.cycle)
# print(layout.depth.minor)
# print(layout.depth.scale)
# print(layout.depth.skip)

print(layout.depth.limit)

print(file['DEPT'])

depth,depth_lim = layout.depth(file['DEPT'],limit=(1280,1350))

limit = dw.layout.axis.Multivar.limit(file['DEPT'],power=-1)

length = dw.layout.axis.Binary.length(limit)

print(dw.layout.axis.Unary.ceil(length/10.))

# print(depth)
# print(depth_lim)

# grtot,grtot_lim = layout[0](file['GR-TOT'],)

# heads,bodys = dw.bokeh.boot(layout)

# print(file.keys())

# bodys[0].line(grtot,depth)

# grid = gridplot([heads,bodys],toolbar_location=None)

# show(grid)