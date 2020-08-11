# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:27:40 2020

@author: neash
"""

from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRaisedButton
import numpy as np
import matplotlib.pyplot as plt






"""
corner relative positions
(0.12569444444444444, 0.31298557158712537)
(0.9013888888888889, 0.3140954495005549)
(0.9013888888888889, 0.6892341842397336)
(0.12569444444444444, 0.6892341842397336)
"""


cos=np.cos
sin=np.sin
tan=np.tan
exp=np.exp

class Phase_plot(MDApp):
    



    
    def build(self): 
        self.w=5
        self.xeq="-1 - x**2 + y"
        self.yeq="1 + x - y**2"
        self.title = "Phase Portrait"
        self.theme_cls.theme_style = "Dark" #Dark theme for the app
        self.init_plot()

        return Builder.load_file("string_layout.kv")


    def init_plot(self):
        
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(8, 8))
        fig=self.fig
        w=self.w
        plt.grid()
        plt.axis([-w,w,-w,w])
        fig.canvas.draw()
        # Now we can save it to a numpy array.
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.imsave("flow.png",data)


   
        
    def draw_flow(self,screen_coords):

        fig=self.fig
        w=self.w
        x_coord=(((list(screen_coords)[0]-0.12469)/0.775)-0.5)*2*w
        y_coord=(((list(screen_coords)[1]-0.313)/0.379)-0.5)*2*w
        if x_coord >w or x_coord<-w:
            x_coord=w*np.sign(x_coord)
        if y_coord >w or y_coord<-w:
            y_coord=w*np.sign(y_coord)
        y, x = np.mgrid[-w*1.5:w*1.5:200j, -w*1.5:w*1.5:200j]

        U = eval(self.xeq)
        V = eval(self.yeq)

     
        seed_points = np.array([[x_coord], [y_coord]])
        plt.streamplot(x, y, U, V, color=U, linewidth=2,
                      cmap='autumn', start_points=seed_points.T)
        # Displaying the starting points with blue symbols.
        plt.plot(seed_points[0], seed_points[1], 'bo')
        fig.canvas.draw()
        # Now we can save it to a numpy array.
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.imsave("flow.png",data)
        self.root.ids["im"].reload()

   
            
    def equation_change(self):
        if self.root.ids["textx"].text=="" or self.root.ids["texty"].text=="":
            self.xeq="-1 - x**2 + y"
            self.yeq="1 + x - y**2"
        else:
            textx=str_eqn(self.root.ids["textx"].text)
            texty=str_eqn(self.root.ids["texty"].text)
            self.xeq=textx.parse_eqn()
            self.yeq=texty.parse_eqn()
        
class str_eqn(str):   
    
     def parse_eqn(self):
        return self.replace("^","**")
        

        
class TextX(MDTextField):
    def on_text(*args):
        plotApp.root.ids["setequations"].md_bg_color = 0.14, 0.54, 1, 1
    

class TextY(MDTextField):
    def on_text(*args):
        plotApp.root.ids["setequations"].md_bg_color = 0.14, 0.54, 1, 1

class FullImage(Image):
    pass


class MDButton(MDRaisedButton, TouchBehavior, MDApp):   

    def on_long_touch(self,touch,*args):
        self.duration_long_touch = 0.2
        return plotApp.draw_flow(touch.spos)

class RestartBTN(MDRaisedButton):
    
    def on_press(self):
        plotApp.init_plot()
        return plotApp.root.ids["im"].reload()

class EquationBTN(MDRaisedButton):
    
    def on_press(self):
        self.md_bg_color = .6, .6, .6, .6
        plotApp.init_plot()
        plotApp.root.ids["im"].reload()
        plotApp.equation_change()   
        



plotApp=Phase_plot()


plotApp.run()
