import ephem
import math
 
 
def rad2deg(n):
    return 180*n/math.pi
 
  
class SpaceObject():
    def __init__(self, name):
        self.name = name
        self.lat = None
        self.lon = None
        self.tle = []

    def update_TLE(self):
        self.ephemeris = ephem.readtle(self.tle[0], self.tle[1], self.tle[2])

    def process_TLE(self):
        self.ephemeris.compute()
        self.lat = rad2deg(self.ephemeris.sublat)
        self.lon = rad2deg(self.ephemeris.sublong)

clu1 = SpaceObject("CLU1")
clu1.tle = ("ISS (ZARYA)",
"1 25544U 98067A   16199.82010626  .00004168  00000-0  68389-4 0  9998",
"2 25544  51.6449 265.1961 0001716  65.5653  43.7582 15.54851285  9750")  
 
clu1.update_TLE()
clu1.process_TLE()


def load_image(image_file):
    import numpy as np
    from os.path import join
    from os import getcwd
    from PIL import Image
    
    img_file = Image.open(join(getcwd(), image_file))
    img_width = img_file.width
    img_height = img_file.height
    img_data = list(img_file.getdata())
    img = np.empty((img_height, img_width), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((img_height, img_width, 4))
    for h in range(img_height):
        for w in range(img_width):
            H = img_height-h-1
            view[H, w, 0] = img_data[(h * img_width) + w][0]
            view[H, w, 1] = img_data[(h * img_width) + w][1]
            view[H, w, 2] = img_data[(h * img_width) + w][2]
            view[H, w, 3] = 255
    return img


###########################################


from django.shortcuts import render
from django.http import JsonResponse
from bokeh.models import AjaxDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE

def index(request): 
    plot = figure(responsive=True,
               plot_width=500,
               plot_height=250,
               tools=[],
               x_range=(-180, 180),
               y_range=(-90, 90))
    plot.toolbar_location = None
    plot.axis.visible = None
 
    source = AjaxDataSource(method='GET',
                            data_url='http://localhost:8000/view2d/data/',
                            polling_interval=1000) 
    
    source.data = dict(x=[], y=[]) # workaround
 
    img = load_image("static/images/earth.png") 
    plot.image_rgba(image=[img], x=[-180], y=[-90], dw=[360], dh=[180])
    plot.cross(source=source, x='x', y='y', size=22, line_width=4, color='Orange') # CLU1

    script, div = components(plot, INLINE)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    context = {
        'bokeh_script' : script,
        'bokeh_div' : div,
        'js_resources' : js_resources,
        'css_resources' : css_resources
        }
    
    return render(request, 'view2d/index.html', context)

def data(request): 
    clu1.process_TLE()
    response = JsonResponse(dict(x=[clu1.lon], y=[clu1.lat]))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response
