import os

from jinja2 import Template

from bokeh.embed import components
from bokeh.resources import INLINE

from bokeh.util.browser import view

from bokeh.plotting import figure as bokeh_figure

from bokeh.layouts import gridplot

from bokeh.models import Range1d
from bokeh.models import LinearAxis
from bokeh.models import Label

import lasio

import numpy

class TrackDict:

	width 		: int = 200

	head_height : int = 50
	body_height : int = 15

	head_xrange : tuple[int] = (0,1)
	head_yrange	: tuple[int] = (0,10)

	tooltips 	: list[tuple[str]] = [('@x','@y{1.1}')]
	#[(file.keys()[index+1],'@x'),(file.keys()[0],'@y{1.1}')]

	htmltemp 	: str = (
		'''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8">
				<title>LAS Curves - Bokeh Glance</title>
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

class Trails():

	def __init__(self,filename:str,htmlname:str=None,**kwargs):

		self._file = lasio.read(filename,**kwargs)

		self.filename = filename
		self.htmlname = htmlname

	@property
	def file(self):
		return self._file

	@property
	def filename(self):
		return self._filename

	@filename.setter
	def filename(self,value:str):
		self._filename = value
	
	@property
	def htmlname(self):
		return self._htmlname

	@htmlname.setter
	def htmlname(self,value:str):

		if value is None:
			value = self.filename
		
		self._htmlname = os.path.splitext(value)[0]+'.html'
	
	def __getitem__(self,key):
		return self.file[key]

	@property
	def number(self):
		return len(self.file.keys())

	@property
	def depths(self):
		return self.file[0]

	@property
	def maxdepth(self):
		return numpy.nanmax(self.depths)

	@property
	def mindepth(self):
		return numpy.nanmin(self.depths)

	@property
	def length(self):
		return int(self.maxdepth-self.mindepth)
	
	def __call__(self,**kwargs):

		self.track = kwargs

		self.template = self.track.htmltemp

		heads = [self.head(index) for index in range(1,self.number)]
		bodys = [self.body(index) for index in range(1,self.number)]

		grid = gridplot([heads,bodys],toolbar_location=None)

		script,div = components(grid)

		htmltemp = self.template.render(
			java 	= self.java,
			css 	= self.css,
			script 	= script,
			div 	= div
			)

		with open(self.htmlname,'w') as htmlfile:
			htmlfile.write(htmltemp)

		return self

	@property
	def track(self):
		return self._track

	@track.setter
	def track(self,value:dict):
		self._track = TrackDict(**value)

	@property
	def height(self):
		return (self.track.head_height,self.track.body_height*self.length)

	@property
	def template(self):
		return self._template

	@template.setter
	def template(self,value:str):
		self._template = Template(value)
	
	def head(self,index):

		figure = bokeh_figure(
			width=self.track.width,height=self.height[0])

		figure = self.boothead(figure)

		figure = self.loadhead(figure,index)

		return figure

	def body(self,index):

		figure = bokeh_figure(
			width=self.track.width,height=self.height[1],tooltips=self.track.tooltips)

		figure = self.bootbody(figure)
			
		figure = self.loadbody(figure,index)

		return figure

	def boothead(self,figure:bokeh_figure):

		figure = self.deactivate(figure)

		figure.x_range = Range1d(*self.track.head_xrange)
		figure.y_range = Range1d(*self.track.head_yrange)

		figure.xaxis.visible = False
		figure.yaxis.visible = False

		figure.xgrid.grid_line_color = None
		figure.ygrid.grid_line_color = None

		return figure

	def bootbody(self,figure:bokeh_figure):

		figure = self.deactivate(figure)

		figure.add_layout(LinearAxis(major_label_text_alpha=0),'right')
		figure.add_layout(LinearAxis(),'above')

		figure.y_range.flipped = True

		figure.ygrid.minor_grid_line_color = 'lightgray'
		figure.ygrid.minor_grid_line_alpha = 0.2

		figure.ygrid.grid_line_color = 'lightgray'
		figure.ygrid.grid_line_alpha = 1.0

		return figure

	def loadhead(self,figure:bokeh_figure,index:int):

		text = self.file.keys()[index]

		y_offset = self.track.head_yrange[0]-self.track.head_yrange[1]

		labels = Label(x=0.5,y=5,text=text,text_align="center",y_offset=y_offset)

		figure.add_layout(labels)

		return figure

	def loadbody(self,figure:bokeh_figure,index:int):

		figure.line(self.file[index],self.file[0])

		return figure

	@staticmethod
	def deactivate(figure:bokeh_figure):

		figure.toolbar.active_drag = None
		figure.toolbar.active_scroll = None
		figure.toolbar.active_tap = None

		return figure

	@property
	def java(self):
		return INLINE.render_js()

	@property
	def css(self):
		return INLINE.render_css()

	def show(self):
		view(self.htmlname)