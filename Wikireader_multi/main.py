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
from kivy.uix.screenmanager import ScreenManager, Screen

LabelBase.register(name="raleway",
                   fn_regular="Raleway-Regular.ttf",fn_bold="Raleway-Bold.ttf")


class MenuScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name = 'menu'))
sm.add_widget(ProfileScreen(name = 'profile'))

class WikiReaderApp(MDApp):
    
    def change_lang(self,lang):
        self.lang=lang
    
               

    def build(self):
        self.lang=None
        self.title = "Wikipedia Reader"
        self.theme_cls.theme_style = "Dark" #Dark theme for the app
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        return Builder.load_file("screen_string.kv")
        

        
        
    def random_search_button(self):
        endpoint = f"https://{self.lang}.wikipedia.org/w/api.php?action=query&list=random&rnlimit=1&rnnamespace=0&format=json"
        
        self.root.current_screen.ids["mdtit"].text = "Random search: please wait"
        self.root.current_screen.ids["mdlab"].text = ""
        self.root.current_screen.ids["mdbu"].text = "Please wait..."
        self.root.current_screen.ids["mdbu"].md_bg_color = 0.6, 0.6, 0.6, 0.6
        self.rs_request = UrlRequest(endpoint,
                                     on_success=self.get_data,
                                     ca_file = certifi.where())
        
    def get_data(self,request,response):
        random_article = response["query"]["random"][0]
        random_title = random_article["title"]
        endpoint = f"https://{self.lang}.wikipedia.org/w/api.php?prop=extracts&explaintext&exintro&format=json&action=query&titles={random_title.replace(' ', '%20')}"
        self.rs_request = UrlRequest(endpoint,
                                     on_success=self.set_textarea,
                                     ca_file = certifi.where())
        
    def set_textarea(self,request,response):
        page_info = response["query"]["pages"]
        page_id = next(iter(page_info))
        page_title = page_info[page_id]["title"]
        page_extract = page_info[page_id]["extract"]
        self.root.current_screen.ids["mdbu"].text = "Random Search"
        self.root.current_screen.ids["mdbu"].md_bg_color = 0.14, 0.54, 1, 1
        self.root.current_screen.ids["mdtit"].text =f"{page_title}"
        self.root.current_screen.ids["mdlab"].text = f"{page_extract}"
        
WikiReaderApp().run()











