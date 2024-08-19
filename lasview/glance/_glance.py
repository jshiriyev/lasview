import os

from jinja2 import Template

from bokeh.embed import components
from bokeh.resources import INLINE

from bokeh.util.browser import view

from bokeh.plotting import figure as bhfig

from bokeh.layouts import gridplot

from bokeh.models import Range1d
from bokeh.models import LinearAxis
from bokeh.models import Label

import lasio

class GlanceCurveDict:

	width 		: int = 200
	height 		: tuple[int] = (50,None)

	headXrange 	: tuple[int] = (0,1)
	headYrange	: tuple[int] = (0,10)

	tooltips 	: list[tuple[str]] = [('@x','@y{1.1}')]
	htmltemp 	: str = (
		'''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8">
				<title>Bokeh LAS Curve Glance</title>
				{{ java }}
				{{ css }}
				{{ script }}
			<style>
			.wrapper {
				display: flex;
				justify-content: center;
				align-items: center;
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
		'''
		)

class Glance(GlanceCurveDict):

	def __init__(self,filename:str,htmlname:str=None,**kwargs):

		super().__init__()

		kwargs['file_ref'] = filename

		self.file = kwargs

		self.html = filename if htmlname is None else htmlname

		self.temp = self.htmltemp

	@property
	def file(self):
		return self._file

	@file.setter
	def file(self,value:dict):
		self._file = lasio.read(**value)

	@property
	def html(self):
		return self._html

	@html.setter
	def html(self,value:str):
		self._html = os.path.splitext(value)[0]+'.html'
	
	@property
	def temp(self):
		return self._temp

	@temp.setter
	def temp(self,value:str):
		self._temp = Template(value)
	
	def __getitem__(self,key):
		return self.file[key]

	@property
	def trails(self):
		return len(self.file.keys())

	@property
	def depths(self):
		return self.file[0]

	@property
	def length(self):
		return int(self.depths[-1]-self.depths[0])
	
	def __call__(self,**kwargs):

		super().__init__(**kwargs)

		heads,bodys = [],[]

		head_height,body_height = self.height

		body_height = 15 if body_height is None else body_height

		for index in range(self.trails-1):

			head = bhfig(width=self.width,height=head_height)
			body = bhfig(width=self.width,height=body_height*self.length,
				tooltips=self.tooltips)
			#[(file.keys()[index+1],'@x'),(file.keys()[0],'@y{1.1}')]

			head = self.deactivate(head)
			body = self.deactivate(body)

			body.add_layout(LinearAxis(major_label_text_alpha=0),'right')
			body.add_layout(LinearAxis(),'above')

			head.x_range = Range1d(*self.headXrange)
			head.y_range = Range1d(*self.headYrange)

			head.xaxis.visible = False
			head.yaxis.visible = False

			body.y_range.flipped = True

			head.xgrid.grid_line_color = None
			head.ygrid.grid_line_color = None

			body.ygrid.minor_grid_line_color = 'lightgray'
			body.ygrid.minor_grid_line_alpha = 0.2

			body.ygrid.grid_line_color = 'lightgray'
			body.ygrid.grid_line_alpha = 1.0

			body.line(self.file[index+1],self.file[0])

			y_offset = self.headYrange[0]-self.headYrange[1]

			labels = Label(x=0.5,y=5,text=self.file.keys()[index+1],text_align="center",y_offset=y_offset)

			head.add_layout(labels)

			heads.append(head)
			bodys.append(body)

		grid = gridplot([heads,bodys],toolbar_location=None)

		script,div = components(grid)

		htmltemp = self.temp.render(
			java 	= self.java,
			css 	= self.css,
			script 	= script,
			div 	= div
			)

		with open(self.html,'w') as htmlfile:
			htmlfile.write(htmltemp)

	@property
	def java(self):
		return INLINE.render_js()

	@property
	def css(self):
		return INLINE.render_css()

	@staticmethod
	def deactivate(figure:bhfig):

		figure.toolbar.active_drag = None
		figure.toolbar.active_scroll = None
		figure.toolbar.active_tap = None

		return figure

	def show(self):
		view(self.html)