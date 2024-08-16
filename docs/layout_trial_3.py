from bokeh.io import curdoc

from bokeh.plotting import show
from bokeh.plotting import output_file

from bokeh.layouts import gridplot
from bokeh.layouts import column
from bokeh.layouts import Row, Column

from bokeh.models import Div
from bokeh.models import Range1d
from bokeh.models import LinearAxis
from bokeh.models import Label



from bokeh.plotting import figure

import lasio

file = lasio.read('digitized_data.las')


print(file.keys())

print(file[0])

trail = 6

heads,bodys = [],[]

for index in range(trail-1):

	head = figure(width=200,height=50)
	body = figure(width=200,height=1000)

	head.add_layout(LinearAxis(major_label_text_alpha=0),'right')
	head.add_layout(LinearAxis(major_label_text_alpha=0),'above')

	body.add_layout(LinearAxis(major_label_text_alpha=0),'right')
	body.add_layout(LinearAxis(major_label_text_alpha=0),'above')

	head.y_range = Range1d(0,10)
	body.y_range = Range1d(1340,1280)

	head.x_range = Range1d(0,1)
	# body.x_range = Range1d(0,1)

	head.xgrid.grid_line_color = None
	head.ygrid.grid_line_color = None

	head.xaxis.major_label_text_font_size = '0pt'
	head.yaxis.major_label_text_font_size = '0pt'

	# body.xaxis.major_label_text_font_size = '0pt'
	# body.yaxis.major_label_text_font_size = '0pt'

	head.xaxis.major_tick_in = 0
	head.yaxis.major_tick_in = 0
	# body.xaxis.major_tick_in = 0
	# body.yaxis.major_tick_in = 0

	head.xaxis.major_tick_out = 0
	head.yaxis.major_tick_out = 0
	# body.xaxis.major_tick_out = 0
	# body.yaxis.major_tick_out = 0

	head.xaxis.minor_tick_in = 0
	head.yaxis.minor_tick_in = 0
	# body.xaxis.minor_tick_in = 0
	# body.yaxis.minor_tick_in = 0

	head.xaxis.minor_tick_out = 0
	head.yaxis.minor_tick_out = 0
	# body.xaxis.minor_tick_out = 0
	# body.yaxis.minor_tick_out = 0

	# if index==0:
	# 	head.min_border_left = 500
	# else:
	# 	head.min_border_left = 0

	# if index!=trail-1:
	# 	head.min_border_right = 0

	# head.min_border_top = 0
	# head.min_border_bottom = 0

	# if index==0:
	# 	body.min_border_left = 500
	# else:
	# 	body.min_border_left = 0

	# if index!=trail-1:
	# 	body.min_border_right = 0
	
	# body.min_border_top = 0
	# # body.min_border_bottom = 0

	# head.line((0,20),(10,10))
	# head.line((0,20),(20,20))

	body.line(file[index+1],file[0])

	labels = Label(x=0.5,y=5,text=file.keys()[index+1],text_align="center",y_offset=-10)#x_offset=-5, y_offset=-10)

	head.add_layout(labels)

	heads.append(head)
	bodys.append(body)

grid = gridplot([heads,bodys],toolbar_location=None)

# centered_div = Div(
#     text="""
#     <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
#         <div style="text-align: center;">
#         </div>
#     </div>
#     """
# )

# layout = column(centered_div, grid)

# output_file("layout_trial_3.html")

# show(Column(Row(*heads),Row(*bodys)))

show(grid,responsive = True)