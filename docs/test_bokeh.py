from jinja2 import Template
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.browser import view

x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]

p1 = figure(width=300, height=300)
p1.scatter(x1, y1, size=12, color="red", alpha=0.5)

script, div = components(p1)

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
        width: 800px;
        background-color: yellow;
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

filename = 'embed_multiple.html'

html = template.render(js_resources=js_resources,
                       css_resources=css_resources,
                       script=script,
                       div=div)

with open(filename, 'w') as f:
    f.write(html)

view(filename)