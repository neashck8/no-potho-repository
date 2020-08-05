# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 16:22:52 2020

@author: neash

pip install kivy==2.0.0rc3
pip install kivymd==0.104.1
pip install docutils pygments pypiwin32 kivy.deps.sdl2
pip install kivy.deps.glew
"""
import certifi
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.network.urlrequest import UrlRequest

LabelBase.register(name="raleway",
                   fn_regular="Raleway-Regular.ttf",fn_bold="Raleway-Bold.ttf")




class WikiReaderApp(MDApp):
    
               

    def build(self):
        self.title = "Wikipedia Reader"
        self.theme_cls.theme_style = "Dark" #Dark theme for the app
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        return Builder.load_file("random_search_screen.kv")
        

        
        
    def random_search_button(self):
        endpoint = "https://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=1&rnnamespace=0&format=json"
        self.root.ids["mdtit"].text = "Random search: please wait"
        self.root.ids["mdlab"].text = ""
        self.root.ids["mdbu"].text = "Please wait..."
        self.root.ids["mdbu"].md_bg_color = 0.6, 0.6, 0.6, 0.6
        self.rs_request = UrlRequest(endpoint,
                                     on_success=self.get_data,
                                     ca_file = certifi.where())
        
    def get_data(self,request,response):
        random_article = response["query"]["random"][0]
        random_title = random_article["title"]
        endpoint = f"https://en.wikipedia.org/w/api.php?prop=extracts&explaintext&exintro&format=json&action=query&titles={random_title.replace(' ', '%20')}"
        self.rs_request = UrlRequest(endpoint,
                                     on_success=self.set_textarea,
                                     ca_file = certifi.where())
        
    def set_textarea(self,request,response):
        page_info = response["query"]["pages"]
        page_id = next(iter(page_info))
        page_title = page_info[page_id]["title"]
        page_extract = page_info[page_id]["extract"]
        self.root.ids["mdbu"].text = "Random Search"
        self.root.ids["mdbu"].md_bg_color = 0.14, 0.54, 1, 1
        self.root.ids["mdtit"].text =f"{page_title}"
        self.root.ids["mdlab"].text = f"{page_extract}"
        
WikiReaderApp().run()











