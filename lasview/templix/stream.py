from jinja2 import Template

from bokeh.embed import components
from bokeh.resources import INLINE

from bokeh.util.browser import view

from bokeh.plotting import figure

from bokeh.layouts import gridplot

from bokeh.models import Range1d
from bokeh.models import LinearAxis
from bokeh.models import Label

import lasio

file = lasio.read('sample.las')

trail = len(file.keys())

heads,bodys = [],[]

for index in range(trail-1):

	head = figure(width=200,height=50)
	body = figure(width=200,height=1000,tooltips=[(file.keys()[index+1],'@x'),(file.keys()[0],'@y{1.1}')])

	head.toolbar.active_drag = None
	head.toolbar.active_scroll = None
	head.toolbar.active_tap = None

	body.toolbar.active_drag = None
	body.toolbar.active_scroll = None
	body.toolbar.active_tap = None

	body.add_layout(LinearAxis(major_label_text_alpha=0),'right')
	body.add_layout(LinearAxis(),'above')

	head.x_range = Range1d(0,1)
	head.y_range = Range1d(0,10)

	head.xaxis.visible = False
	head.yaxis.visible = False

	# body.y_range = Range1d(1340,1280)
	body.y_range.flipped = True

	head.xgrid.grid_line_color = None
	head.ygrid.grid_line_color = None

	body.ygrid.minor_grid_line_color = 'lightgray'
	body.ygrid.minor_grid_line_alpha = 0.2

	body.ygrid.grid_line_color = 'lightgray'
	body.ygrid.grid_line_alpha = 1.0

	body.line(file[index+1],file[0])

	labels = Label(x=0.5,y=5,text=file.keys()[index+1],text_align="center",y_offset=-10)

	head.add_layout(labels)

	heads.append(head)
	bodys.append(body)

grid = gridplot([heads,bodys],toolbar_location=None)

script,div = components(grid)

template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Bokeh Scatter Plots</title>
        {{ js_resources }}
        {{ css_resources }}
        {{ script }}
    <style>
    .wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        # background-color: yellow;
        margin: 0 auto;
        }
    .plotdiv {
        margin: 0 auto;
        }
    </style>
    </head>
    <body>
    <div class='wrapper'>
        {{ div }}
    </div>
    </body>
</html>
''')

js_resources = INLINE.render_js()
css_resources = INLINE.render_css()

filename = 'depthwise.html'

html = template.render(
	js_resources=js_resources,
    css_resources=css_resources,
    script=script,
    div=div)

with open(filename,'w') as f:
    f.write(html)

view(filename)