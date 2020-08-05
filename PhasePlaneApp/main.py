# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:27:40 2020

@author: neash
"""
from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRaisedButton
import numpy as np
import matplotlib.pyplot as plt



plt.style.use('dark_background')
w = 5
fig = plt.figure()
plt.grid()
plt.axis([-w,w,-w,w])


"""
corner relative positions
(0.12569444444444444, 0.31298557158712537)
(0.9013888888888889, 0.3140954495005549)
(0.9013888888888889, 0.6892341842397336)
(0.12569444444444444, 0.6892341842397336)
"""

class FullImage(Image):
    pass


class MDButton(MDRaisedButton, TouchBehavior, MDApp):   

    def on_long_touch(self,touch,*args):
        self.duration_long_touch = 0.1
        return plotApp.draw_flow(touch.spos)

    

class Phase_plot(MDApp):
    
    def build(self): 
        self.title = "Phase Portrait"
        self.theme_cls.theme_style = "Dark" #Dark theme for the app
        self.init_plot()
        return Builder.load_file("string_layout.kv")

    
    def init_plot(self):
        #w = 5
        #self.fig = plt.figure()
        #print(vars(self))
        #plt.grid()
        #plt.axis([-w,w,-w,w])
        fig.canvas.draw()
        # Now we can save it to a numpy array.
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.imsave("flow.png",data)

   
        
    def draw_flow(self,screen_coords):
        x_coord=(((list(screen_coords)[0]-0.12469)/0.775)-0.5)*10
        y_coord=(((list(screen_coords)[1]-0.313)/0.379)-0.5)*10

        Y, X = np.mgrid[-w:w:100j, -w:w:100j]
        U = -1 - X**2 + Y
        V = 1 + X - Y**2

     
        seed_points = np.array([[x_coord], [y_coord]])
        plt.streamplot(X, Y, U, V, color=U, linewidth=2,
                      cmap='autumn', start_points=seed_points.T)
        # Displaying the starting points with blue symbols.
        plt.plot(seed_points[0], seed_points[1], 'bo')
        fig.canvas.draw()
        # Now we can save it to a numpy array.
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.imsave("flow.png",data)
        plt.imsave("flow_alt.png",data)
        self.root.ids["im"].reload()
            
            
            





plotApp=Phase_plot()


plotApp.run()
