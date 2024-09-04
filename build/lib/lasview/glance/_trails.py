from dataclasses import dataclass, field

import os

from jinja2 import Template

from bokeh.embed import components
from bokeh.resources import INLINE

from bokeh.util import browser

from bokeh.plotting import figure as bokeh_figure

from bokeh.layouts import gridplot

from bokeh.models import Div

from bokeh.models import Range1d
from bokeh.models import LinearAxis
from bokeh.models import Label

import lasio

import numpy

@dataclass
class Frame:
	"""Dictionary for general frame construction."""

	width 		: int = 200

	hheight 	: int = 50
	bheight 	: int = 15

	hsticky 	: bool = True

	hxrange 	: tuple[int] = (0,1)
	hyrange		: tuple[int] = (0,1)

class Trails():

	def __init__(self,filename:str,htmlname:str=None,**kwargs):

		self._file = lasio.read(filename,**kwargs)

		self.filename = filename
		self.htmlname = htmlname

		self.build()

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

	def index(self,key):
		return self.file.keys().index(key)-1

	@property
	def curves(self):
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
	def depth(self):
		return int(self.maxdepth-self.mindepth)

	def build(self,**kwargs):

		self.frame = kwargs

		self.lines = []

		self.heads = [self.head(index) for index in range(1,self.curves)]
		self.bodys = [self.body(index) for index in range(1,self.curves)]

	@property
	def frame(self):
		return self._frame

	@frame.setter
	def frame(self,value:dict):
		self._frame = Frame(**value)

	@property
	def height(self):
		return (self.frame.hheight,self.frame.bheight*self.depth)

	def style(self,key:str,**kwargs):

		for name,value in kwargs.items():
			setattr(self.lines[self.index(key)].glyph,f"line_{name}",value)

	def color(self,key:str,cut:float,left:bool=True,**kwargs):

		conds = self[key]<cut if left else self[key]>cut

		z1 = numpy.where(conds,self[key],cut)
		z2 = numpy.full_like(z1,cut)

		x1 = z1 if left else z2
		x2 = z2 if left else z1

		self.bodys[self.index(key)].harea(y=self.depths,x1=x1,x2=x2,**kwargs)

	def tieup(self,key:str,tokey:str,multp:float=1,shift:float=0,line:dict=None,left:bool=None,**kwargs):

		value = self[key]*multp+shift

		style = {f"line_{name}":value for name,value in (line or {}).items()}

		self.bodys[self.index(tokey)].line(value,self.depths,**style)

		if left is None:
			return

		conds = value<self[tokey] if left else value>self[tokey]

		z1 = numpy.where(conds,value,self[tokey])
		z2 = numpy.full_like(z1,self[tokey])

		x1 = z1 if left else z2
		x2 = z2 if left else z1

		self.bodys[self.index(tokey)].harea(y=self.depths,x1=x1,x2=x2,**kwargs)
	
	def head(self,index):

		width,height = self.frame.width,self.height[0]

		if index==1:
			width += int(width/6)

		sticky_css = {'position':'sticky','top':'0px','z-index':'1000'}

		styles = sticky_css if self.frame.hsticky else {}

		figure = bokeh_figure(width=width,height=height,styles=styles)

		figure = self.boothead(figure,index)
		figure = self.loadhead(figure,index)

		return figure

	def body(self,index):

		width,height = self.frame.width,self.height[1]

		if index==1:
			width += int(width/6)

		figure = bokeh_figure(width=width,height=height,
			tooltips = [(self.file.keys()[index],'@x'),('Depth','@y{1.1}')]
			)

		figure = self.bootbody(figure,index)
		figure = self.loadbody(figure,index)

		return figure

	def boothead(self,figure:bokeh_figure,index:int):

		figure = self.deactivate(figure)

		figure.x_range = Range1d(*self.frame.hxrange)
		figure.y_range = Range1d(*self.frame.hyrange)

		figure = self.trim(figure,"x")
		figure = self.trim(figure,"y")

		figure.add_layout(self.bold,'above')
		figure.add_layout(self.bold,'right')

		figure.xgrid.grid_line_color = None
		figure.ygrid.grid_line_color = None

		return figure

	def bootbody(self,figure:bokeh_figure,index:int):

		figure = self.deactivate(figure)

		figure.add_layout(LinearAxis(),'above')

		if index>1:
			figure = self.trim(figure,"y")

		figure.add_layout(self.bold,'right')

		figure.y_range = Range1d(self.maxdepth,self.mindepth)

		figure.yaxis.ticker.max_interval = 20

		figure.ygrid.minor_grid_line_color = 'lightgray'
		figure.ygrid.minor_grid_line_alpha = 0.2

		figure.ygrid.grid_line_color = 'lightgray'
		figure.ygrid.grid_line_alpha = 1.0

		return figure

	def loadhead(self,figure:bokeh_figure,index:int):

		text = self.file.keys()[index]

		x = numpy.mean(self.frame.hxrange)
		y = numpy.mean(self.frame.hyrange)

		labels = Label(x=x,y=y,text=text,text_align='center',text_baseline="middle")

		figure.add_layout(labels)

		return figure

	def loadbody(self,figure:bokeh_figure,index:int):

		self.lines.append(figure.line(self.file[index],self.depths))

		return figure

	@staticmethod
	def deactivate(figure:bokeh_figure):

		figure.toolbar.active_drag = None
		figure.toolbar.active_scroll = None
		figure.toolbar.active_tap = None

		return figure

	@staticmethod
	def trim(figure:bokeh_figure,axis="x"):

		getattr(figure,f"{axis}axis").major_tick_line_alpha = 0
		getattr(figure,f"{axis}axis").minor_tick_line_alpha = 0
		getattr(figure,f"{axis}axis").major_label_text_alpha = 0

		return figure

	def wrapup(self):

		grid = gridplot([self.heads,self.bodys],toolbar_location=None)

		script,div = components(grid)

		return self.template.render(
			java=self.java,css=self.css,script=script,div=div)

	@property
	def template(self):
		return Template(
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

	@property
	def bold(self):
		return LinearAxis(
			major_tick_line_alpha=0,
			minor_tick_line_alpha=0,
			major_label_text_alpha=0,
			)

	@property
	def java(self):
		return INLINE.render_js()

	@property
	def css(self):
		return INLINE.render_css()

	def show(self):

		htmltext = self.wrapup()

		with open(self.htmlname,'w') as htmlfile:
			htmlfile.write(htmltext)

		browser.view(self.htmlname)