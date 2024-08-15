from bokeh.plotting import show

from bokeh.layouts import gridplot

import lasio

from lasview import depthwise as dw

file = lasio.read('digitized_data.las')

wizard = dw.Wizard(file,
	ntrails = 4,
	ncurves = 3,
	# depth = dict(values=file['DEPT'],spot=1),
	width = (100,250),
	height = (50,50),
	)

print(wizard.ntrails)
print(wizard.ncurves)
print(wizard.depth.curve)

# print(wizard.depth.spot)
# print(wizard.depth.cycle)
# print(wizard.depth.minor)
# print(wizard.depth.scale)
# print(wizard.depth.skip)

# print(wizard.depth.limit)

# print(file['DEPT'])

# depth,depth_lim = wizard.depth(file['DEPT'],limit=(1280,1350))

# limit = dw.wizard.axis.Multivar.limit(file['DEPT'],power=-1)

# length = dw.wizard.axis.Binary.length(limit)

# print(dw.wizard.axis.Unary.ceil(length/10.))

# print(depth)
# print(depth_lim)

# grtot,grtot_lim = wizard[0](file['GR-TOT'],)

# heads,bodys = dw.bokeh.boot(wizard)

# print(file.keys())

# bodys[0].line(grtot,depth)

# grid = gridplot([heads,bodys],toolbar_location=None)

# show(grid)