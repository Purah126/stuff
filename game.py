
'''simple tkinter game wrapper for some reason
see tkinter docs, use  methods of Screen object to create Item subclasses'''

import tkinter as tk
from tkinter.constants import *

class Screen:
    
    def __init__(self, height, width, bg):
        self.height = int(height)
        self.width = int(width)
        self.bg = '#' + str(bg)
        self.root = tk.Tk()
        self.c = tk.Canvas(self.root, height=height, width=width, bg=bg)
        self.c.pack()
    
    def config(self, option, new=None):
        if new == None:
            if option == 'height': return self.height
            elif option == 'width': return self.width
            elif option == 'bg': return self.bg
        else:
            if option == 'height': self.height = int(new)
            elif option == 'width': self.width = int(new)
            elif option == 'bg': self.bg = int(new)
            self.c[height] = self.height
            self.c[width] = self.width
            self.c[bg] = self.bg

class Item:
    
    '''item on a Screen
    use [] to set attributes and methods to get stuff'''
    
    attr = []
    
    def __init__(self, c, num, root):
        self.c = c
        self.num = num
        self.root = root
        self.image_fp = ''
    
    def __getitem__(self, item):
        if item not in type(self).__name__.attr + ['state']:
            raise ValueError(f'Cannot set nonexistant value {item}')
        if item == 'image':
            return self.image_fp
        return self.c.itemcget(self.num, item)
    
    def __setitem__(self, item, value):
        if item not in type(self).__name__.attr + ['state']:
            raise ValueError(f'Cannot set nonexistant value {item}')
        if item == 'image':
            self.image_fp = value
            value = tk.PhotoImage(self.root, file=value)
        return self.c.itemconfigure(self.num, item, value)
    
    def coords(self):
        return self.c.bbox(self.num)
    
    def move(self, x, y):
        self.c.move(self.num, x, y)
    
    def moveto(self, x, y):
        x1, y1, x2, y2 = self.coords()
        self.c.move(self.num, abs(x - x1), abs(y - y1))
    
    def disable(self):
        self['state'] = tk.DISABLED
    
    def enable(self):
        self['state'] = tk.ENABLED

adattr = ['activedash', 'activefill', 'activeoutline', 'activeoutlinestipple', 'activewidth', \
          'disableddash', 'disabledfill', 'disabledoutline', 'disabledoutlinestipple', \
          'disabledstipple', 'disabledwidth']

class Arc(Item):

    attr = ['dash', 'dashoffset', 'disableddash', 'disabledfill', 'extent', 'fill', 'offset', \
            'outline', 'outlineoffset', 'outlinestipple', 'start', 'stipple', 'style', 'width'] + \
            adattr

class Image(Item):
    
    attr = ['activeimage', 'anchor', 'disabledimage']

class Line(Item):
    
    attr = ['arrow', 'arrowshape', 'capstyle', 'dash', 'dashoffset', \
            'fill', 'joinstyle', 'offset', 'splinesteps', 'stipple', 'width'] + adattr

class Oval(Item):
    
    attr = adattr + ['dash', 'dashoffset', 'fill', 'offset', 'outline', 'outlineoffset', \
                     'stipple', 'outlinestipple', 'width']

class Polygon:
    
    attr = adattr + ['dash', 'dashoffset', 'fill', 'joinstyle', 'offset', 'outline', 'outlineoffset', \
                     'smooth', 'splinesteps', 'stipple', 'width']

class Rectangle:
    
    attr = adattr + ['dash', 'dashoffset', 'fill', 'offset', 'outline', 'outlineoffset', \
                     'outlinestipple', 'stipple', 'width']
                     
class Text:
    
    attr = ['activefill', 'activestipple', 'anchor', 'disabledfill', 'disabledstipple', 'fill', \
            'font', 'justify', 'offset', 'stipple', 'text', 'width']
    
class Tag:
    
    '''Tag that contains and operates on multiple Items'''
    
    def __init__(self, name):
        self.name = name
        
    def __getitem__(self, item):
        if item not in type(self).__name__.attr + ['state']:
            raise ValueError(f'Cannot set nonexistant value {item}')
        if item == 'image':
            return self.image_fp
        return self.c.itemcget(self.name, item)
    
    def __setitem__(self, item, value):
        if item not in type(self).__name__.attr + ['state']:
            raise ValueError(f'Cannot set nonexistant value {item}')
        if item == 'image':
            self.image_fp = value
            value = tk.PhotoImage(self.root, file=value)
        return self.c.itemconfigure(self.name, item, value)
    
    def coords(self):
        return self.c.bbox(self.num)
    
    def move(self, x, y):
        self.c.move(self.num, x, y)
    
    def moveto(self, x, y):
        x1, y1, x2, y2 = self.coords()
        self.c.move(self.name, abs(x - x1), abs(y - y1))
    
    def disable(self):
        self['state'] = tk.DISABLED
    
    def enable(self):
        self['state'] = tk.ENABLED
    
    def add(self, other):
        other.c.addtag_withtag(self.name, other.name if type(other) == Tag else other.num)
        self.c = other.c
    
    def delete(self):
        if not hasattr(self, c):
            raise ValueError('Cannot delete tag that has always been empty')
    
    def remove(self, other):
        other.c.dtag(other.num, self.name)
