import json
import pandas as pd
import dearpygui.dearpygui as dpg
import os
import subprocess
import webbrowser
import time
import re
import easygui
import requests
import io
import configparser
import shutil
from pathlib import Path
from screeninfo import get_monitors
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from urllib.error import URLError
from pygame import mixer
from pygame import error
from pathvalidate import sanitize_filepath
from pymongo import MongoClient
from pymongo.errors import InvalidURI,ConfigurationError,OperationFailure,ServerSelectionTimeoutError
from pymongo.client_session import ClientSession
from PIL import Image

print("-----------------------------------------")
print("Welcome to Touhou Music Database") 
print("-----------------------------------------")
mixer.init(frequency=48000,channels=2)

for m in get_monitors():
        Monitor = m
        if 'is_primary=True' in str(Monitor):
                res = str(Monitor)

GLOBALWidth = str(res[18:28]).split("width=")[1]
GLOBALHeight = str(res[29:41]).split("height=")[1]
GLOBALWidth = GLOBALWidth.rstrip(',')
GLOBALHeight = GLOBALHeight.rstrip(',')
time.sleep(0.1)
Resolution = GLOBALWidth +"x"+ GLOBALHeight

GUITitle = None                                
GUICircle = None                               
GUIAlbum = None                                
GUIArrangement = None                          
GUIReleased = None                             
GUIGenre = None                                
GUIOriginal = None                             
GUICharacter = None                            
GUIArtist = None                               
GUIVocalist = None                             
GUIIllustrator = None                          
GUIVideo = None                                
GUILink = None                                 

ViewPortWidth = 0                              
TimesLoaded = 0                                
Volume = 0.1                                   
ToF = 0                                        
GlobalCounter = 0                              

JsonLoaded = False                             
LoadJsonButtonClicked = False                  
ConnectionDB = False                           
DBFiles = False                                
flag1 = False                                  
Flag_MusicPlayerWindow = False                 

TextureTagImage = "texture_tag"                
UserNameL = "Not logged"                       
DLPath = ""                                    

ItemsList = ['None']                           


if DLPath == "":                               
        DLPath = "./DL/"                       
        print("Current DL path: ",DLPath)      


def _GUITitle(sender, app_data, user_data):    
        global GUITitle                        
        global PlaylistTitle                   
        print(f"sender: {sender}, \t Title app_data: {app_data}, \t user_data: {user_data}")                                            
        GUITitle = app_data                    
        if sender == "PlaylistNewTitle" or sender == 383:                                                                               
                PlaylistTitle = app_data       
def _GUICircle(sender, app_data, user_data):   
        global GUICircle                       
        print(f"sender: {sender}, \t Circle app_data: {app_data}, \t user_data: {user_data}")                                           
        GUICircle = app_data                   
def _GUIAlbum(sender, app_data, user_data):    
        global GUIAlbum                        
        print(f"sender: {sender}, \t Album app_data: {app_data}, \t user_data: {user_data}")                                            
        GUIAlbum = app_data                    
def _GUIArrangement(sender, app_data, user_data):                                                                                       
        global GUIArrangement                  
        print(f"sender: {sender}, \t Arrangement app_data: {app_data}, \t user_data: {user_data}")                                      
        GUIArrangement = app_data              
def _GUIReleased(sender, app_data, user_data): 
        global GUIReleased                     
        print(f"sender: {sender}, \t Released app_data: {app_data}, \t user_data: {user_data}")                                         
        GUIReleased = app_data                 
def _GUIGenre(sender, app_data, user_data):    
        global GUIGenre                        
        print(f"sender: {sender}, \t Genre app_data: {app_data}, \t user_data: {user_data}")                                            
        GUIGenre = app_data                    
def _GUIOriginal(sender, app_data, user_data): 
        global GUIOriginal                     
        print(f"sender: {sender}, \t Original app_data: {app_data}, \t user_data: {user_data}")                                         
        GUIOriginal = app_data                 
def _GUICharacter(sender, app_data, user_data):
        global GUICharacter                    
        print(f"sender: {sender}, \t Character app_data: {app_data}, \t user_data: {user_data}")                                        
        GUICharacter = app_data                
def _GUIArtist(sender, app_data, user_data):   
        global GUIArtist                       
        print(f"sender: {sender}, \t Artist app_data: {app_data}, \t user_data: {user_data}")                                           
        GUIArtist = app_data                   
def _GUIVocalist(sender, app_data, user_data): 
        global GUIVocalist                     
        print(f"sender: {sender}, \t Vocalist app_data: {app_data}, \t user_data: {user_data}")                                         
        GUIVocalist = app_data                 
def _GUILyrics(sender, app_data, user_data):   
        global GUILyrics                       
        print(f"sender: {sender}, \t Lyrics app_data: {app_data}, \t user_data: {user_data}")                                           
        GUILyrics = app_data                   
def _GUIIllustrator(sender, app_data, user_data):                                                                                       
        global GUIIllustrator                  
        print(f"sender: {sender}, \t Illustrator app_data: {app_data}, \t user_data: {user_data}")                                      
        GUIIllustrator = app_data              
def _GUIVideo(sender, app_data, user_data):    
        global GUIVideo                        
        print(f"sender: {sender}, \t Video app_data: {app_data}, \t user_data: {user_data}")                                            
        GUIVideo = app_data                                    
def _GUILink(sender, app_data, user_data):     
        global GUILink                         
        print(f"sender: {sender}, \t Link app_data: {app_data}, \t user_data: {user_data}")                                             
        GUILink = app_data                     
def _Username(sender, app_data, user_data):    
        global UserNameL                       
        print(f"sender: {sender}, \t Title app_data: {app_data}, \t user_data: {user_data}")                                            
        UserNameL = app_data                   
def _Password(sender, app_data, user_data):    
        global PassWordL                       
        PassWordL = app_data                   


def _OpenURL(sender, app_data, user_data):     
        JsonDirectory = './Json/'              
        JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]                                  
        URLList = []                           
        for index, js in enumerate(JsonFiles): 
                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:                                                
                        JsonText = json.load(JsonFile)                                                                                  
                        Jurl = JsonText['Music'][0]['root']['Options']['Link']                                                          
                        URLList.append(Jurl)   
        URLs = pd.DataFrame(URLList)           
        print("URLs\n-------------------------")                                                                                        
        print(URLs)                            
        print(f"sender: {sender},\t, app_data: {app_data}\tuser_data: {user_data}")                                                     
        print("URL has been clicked: "+URLList[user_data]+" !")                                                                         
        webbrowser.open(str(URLList[user_data]))                                                                                        


def _OpenURLDB(sender, app_data, user_data):   
        global LinkList                        
        print("URL has been clicked: "+str(LinkList[user_data])[43:-6]+" !")                                                            
        webbrowser.open(str(LinkList[user_data])[43:-6])                                                                                

def _Config(sender,app_data,user_data):                                                                                 
        print(f'sender: {sender}, app_data: {app_data}, user_data: {user_data}')                                        
        global ViewPortWidth   
        global ViewPortHeight  
        global FullscreenOp    
        global DLpathOp        
        global MaximizeOp      
        global ResolutionOp    
        match str(sender):
                case "MaximizeCheck":                                                                                   
                        print("Maximize checkbox!")                                                                     
                        if app_data:                                                                                    
                                print("Maximize True!")                                                                 
                                dpg.maximize_viewport()                                                                 
                                dpg.disable_item("FullScreenCheck")                                                     
                                dpg.hide_item("ScreenResolutionCombo")                                                  
                                dpg.bind_item_theme(item="FullScreenCheck",theme=disableTheme)                          
                                _CurrentResolution(sender,app_data,user_data)                                           
                                MaximizeOp = "yes"                                                                      
                                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':'yes','Fullscreen':FullscreenOp,'Resolution':ResolutionOp,'Filepath':DLpathOp}                                  
                                with open('Config.ini', 'w') as configfile:                                             
                                        configParser.write(configfile)                                                  
                        else:  
                                print("Maximize False!")                                                                
                                dpg.maximize_viewport()                                                                 
                                dpg.enable_item("FullScreenCheck")                                                      
                                dpg.show_item("ScreenResolutionCombo")                                                  
                                dpg.bind_item_theme(item="FullScreenCheck",theme=SelectedTheme)                         
                                dpg.set_viewport_width(ViewPortWidth)                                                   
                                dpg.set_viewport_height(ViewPortHeight)                                                 
                                _CurrentResolution(sender,app_data,user_data)                                           
                                MaximizeOp = "no"                                                                       
                                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':'yes','Fullscreen':FullscreenOp,'Resolution':ResolutionOp,'Filepath':DLpathOp}                                  
                                with open('Config.ini', 'w') as configfile:                                             
                                        configParser.write(configfile)                                                  
                case "FullScreenCheck":                                                                                 
                        print("Fullscreen checkbox!")                                                                   
                        if app_data:                                                                                    
                                print("Fullscreen True!")                                                               
                                dpg.toggle_viewport_fullscreen()                                                        
                                dpg.disable_item("MaximizeCheck")                                                       
                                dpg.hide_item("ScreenResolutionCombo")                                                  
                                dpg.bind_item_theme(item="MaximizeCheck",theme=disableTheme)                            
                                _CurrentResolution(sender,app_data,user_data)                                           
                                FullscreenOp = "yes"                                                                    
                                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':MaximizeOp,'Fullscreen':'yes','Resolution':ResolutionOp,'Filepath':DLpathOp}                                    
                                with open('Config.ini', 'w') as configfile:                                             
                                        configParser.write(configfile)                                                  
                        else:  
                                print("Fullscreen False")                                                               
                                dpg.toggle_viewport_fullscreen()                                                        
                                dpg.set_viewport_width(ViewPortWidth)                                                   
                                dpg.set_viewport_height(ViewPortHeight)                                                 
                                dpg.enable_item("MaximizeCheck")                                                        
                                dpg.show_item("ScreenResolutionCombo")                                                  
                                dpg.bind_item_theme(item="MaximizeCheck",theme=SelectedTheme)                           
                                dpg.set_viewport_width(ViewPortWidth)                                                   
                                dpg.set_viewport_height(ViewPortHeight)                                                 
                                _CurrentResolution(sender,app_data,user_data)                                           
                                FullscreenOp = "no"                                                                     
                                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':MaximizeOp,'Fullscreen':'no','Resolution':ResolutionOp,'Filepath':DLpathOp}                                     
                                with open('Config.ini', 'w') as configfile:                                             
                                        configParser.write(configfile)                                                  
                case "ScreenResolutionCombo":                                                                           
                        print("Screen resolution combo!")                                                               
                        if app_data == "600x700":                                                                       
                                print("600x700!")                                                                       
                                ViewPortWidth = 600                                                                     
                                ViewPortHeight = 700                                                                    
                                ViewPortResolution = str(ViewPortWidth) +"x"+ str(ViewPortHeight)                       
                                dpg.set_viewport_width(ViewPortWidth)                                                   
                                dpg.set_viewport_height(ViewPortHeight)                                                 
                                _CurrentResolution(sender,app_data,user_data)                                           
                                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ViewPortResolution,'Filepath':DLpathOp}                       
                                with open('Config.ini', 'w') as configfile:                                             
                                        configParser.write(configfile)                                                  
                        elif app_data == "900x900":                                                                     
                                print("900x900!")                                                                       
                                ViewPortWidth = 900                                                                     
                                ViewPortHeight = 900                                                                    
                                ViewPortResolution = str(ViewPortWidth) +"x"+ str(ViewPortHeight)                       
                                dpg.set_viewport_width(ViewPortWidth)                                                   
                                dpg.set_viewport_height(ViewPortHeight)                                                 
                                _CurrentResolution(sender,app_data,user_data)                                           
                                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ViewPortResolution,'Filepath':DLpathOp}                       
                                with open('Config.ini', 'w') as configfile:                                             
                                        configParser.write(configfile)                                                  
                        elif app_data == "1280x720":                                                                    
                                print("1280x720!")                                                                      
                                ViewPortWidth = 1280                                                                    
                                ViewPortHeight = 720                                                                    
                                ViewPortResolution = str(ViewPortWidth) +"x"+ str(ViewPortHeight)                       
                                dpg.set_viewport_width(ViewPortWidth)                                                   
                                dpg.set_viewport_height(ViewPortHeight)                                                 
                                _CurrentResolution(sender,app_data,user_data)                                           
                                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ViewPortResolution,'Filepath':DLpathOp}                       
                                with open('Config.ini', 'w') as configfile:                                             
                                        configParser.write(configfile)                                                  

def _LoginConnection():                                             
        global UserNameL                                            
        global PassWordL                                            
        global ConnectionDB                                         
        global LinkList                                             
        global cluster                                              
        dpg.set_value(item="LoginTextInfo",value="Connecting!")     
        dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,255,31))                                                                      
        if UserNameL == "" or PassWordL == "" or UserNameL == " " or PassWordL == " ":                                                                       
                dpg.set_value(item="LoginTextInfo",value="Input something goddamn!")                                                                         
                dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,0,0))                                                                 
        elif ConnectionDB == True:                                  
                dpg.set_value(item="LoginTextInfo",value="Already connected!")                                                                               
                dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,0,0))                                                                 
        else:                                                       
                try:                                                
                        cluster = MongoClient("mongodb+srv://"+UserNameL+":"+PassWordL+"@thmdbcluster.rk32w.mongodb.net/?retryWrites=true&w=majority")       
                        print(cluster.list_database_names())        
                        time.sleep(0.1)                             
                except InvalidURI:                                  
                        print("Incorrect URI")                      
                        dpg.set_value(item="LoginTextInfo",value="Incorrect URI!")                                                                           
                        dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,0,0))                                                         
                except OSError:                                     
                        print("Firewall might be blocking it!")     
                        dpg.set_value(item="LoginTextInfo",value="[OSerror]Firewall might be blocking the connection!")                                      
                        dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,0,0))                                                         
                except ConfigurationError:                          
                        print("Firewall might be blocking it!")     
                        dpg.set_value(item="LoginTextInfo",value="Timeout error\nFirewall might be blocking the connection!")                                  
                        dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,0,0))                                                         
                except OperationFailure:                            
                        print("Incorrect login credentials")        
                        dpg.set_value(item="LoginTextInfo",value="Incorrect login credentials!")                                                             
                        dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,0,0))                                                         
                except ServerSelectionTimeoutError:                 
                        print("connection closed, Timeout: 30s")    
                        dpg.set_value(item="LoginTextInfo",value="[ServerSelectionTimeoutError]"                                                             
                        "You coudln't connect to DB.\npymongo timed out while waiting for a response from the remote server.\n"                                
                        "Usually this means there is a network issue between your machine and the database.")                                                
                        dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(255,0,0))                                                         
                else:                                               
                        print("Correct conection!")                 
                        dpg.set_value(item="LoginTextInfo",value="Connection was succesful")                                                                 
                        dpg.configure_item(item="LoginTextInfo",tag="LoginTextInfo",color=(0,255,0))                                                         
                        for v in range(7):                          
                                v = v + 1                           
                                dpg.set_value(item="LoginInfo"+str(v),value=UserNameL)                                                                       
                                dpg.configure_item(item="LoginInfo"+str(v),tag="LoginInfo"+str(v),color=(0,255,0))                                           
                        ConnectionDB = True                         
                        dpg.add_button(label="Logout",parent="Login_Menu", callback=_Logout)                                                                 

def _Logout():                                                      
        global ConnectionDB                                         
        global cluster                                              
        global UserNameL                                            
        ConnectionDB = False                                        
        cluster['_end_session']                                     
        UserNameL = "Not logged"                                    
        for v in range(7):                                          
                v = v + 1                                           
                dpg.set_value(item="LoginInfo"+str(v),value=UserNameL)                                                                                       
                dpg.configure_item(item="LoginInfo"+str(v),tag="LoginInfo"+str(v),color=(155,0,0))                                                           


def __configOptions(sender, keyword, user_data):                                       
    widget_type = dpg.get_item_type(sender)                                            
    items = user_data                                                                  
    if widget_type == "mvAppItemType::mvRadioButton":                                  
        value = True                                                                   
    else:                                                                              
        keyword = dpg.get_item_label(sender)                                           
        value = dpg.get_value(sender)                                                  
    if isinstance(user_data, list):                                                    
        for item in items:                                                             
            dpg.configure_item(item, **{keyword: value})                               
    else:                                                                              
        dpg.configure_item(items, **{keyword: value})                                  


def _add_config_options(item, columns, *names, **kwargs):                              
    if columns == 1:                                                                   
        if 'before' in kwargs:                                                         
            for name in names:                                                         
                dpg.add_checkbox(label=name, callback=__configOptions, user_data=item, before=kwargs['before'], default_value=dpg.get_item_configuration(item)[name])           
        else:                                                                          
            for name in names:                                                         
                dpg.add_checkbox(label=name, callback=__configOptions, user_data=item, default_value=dpg.get_item_configuration(item)[name])                                    
    else:                                                                              
        if 'before' in kwargs:                                                         
            dpg.push_container_stack(dpg.add_table(header_row=False, before=kwargs['before']))                                                                                  
        else:                                                                          
            dpg.push_container_stack(dpg.add_table(header_row=False))                  
        for i in range(columns):                                                       
            dpg.add_table_column()                                                     
        for i in range(int(len(names)/columns)):                                       
            with dpg.table_row():                                                      
                for j in range(columns):                                               
                    dpg.add_checkbox(label=names[i*columns + j],                       
                                        callback=__configOptions, user_data=item,      
                                        default_value=dpg.get_item_configuration(item)[names[i*columns + j]])                                                                   
        dpg.pop_container_stack()                                                      



def add_online_image(link, **kwargs):                                                           
    with requests.get(link) as res:                                                             
        img = Image.open(io.BytesIO(res.content)).convert("RGBA")                               
        imgdata = []                                                                            
        for r,g,b,a in img.getdata():                                                           
            imgdata.append(r/255)                                                               
            imgdata.append(g/255)                                                               
            imgdata.append(b/255)                                                               
            imgdata.append(a/255)                                                               
        tex = dpg.add_static_texture(img.width, img.height, imgdata, parent="texreg")           
        dpg.configure_item(item=tex,width=250,height=150)                                       
        return dpg.add_image(tex,parent="ImageThumbnail",tag="Thumbnail", **kwargs)             


def _MusicPlay(sender,app_data,user_data):            
        global Volume                                 
        global yt                                     
        global MusicPlaying                           
        JsonDirectory = './Json/'                     
        JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]                                         
        URLList = []                                  
        for index, js in enumerate(JsonFiles):        
                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:                                                       
                        JsonText = json.load(JsonFile)
                        Jurl = JsonText['Music'][0]['root']['Options']['Link']                                                                 
                        URLList.append(Jurl)          
        V = sender[5:]                                
        sender = re.compile(r'B')                     
        yt = YouTube(user_data)                       
        try:                                          
                Thumbnail = YouTube(user_data).thumbnail_url                                                                                   
        except URLError:                              
                dpg.set_value(item="MusicLoadInfoA",value="URL open error [WinError 10013] most probably a problem with the firewall.")        
        finally:                                      
                pass                                  
        try:                                          
                dpg.delete_item(item="Thumbnail")     
        except SystemError:                           
                print("There's no image loaded.")     
        if sender.findall(r'B'):                      
                print("Load thumbnail!")              
                add_online_image(str(Thumbnail))      
        else:                                         
                print("Do not load the thumnail")     
                                                     
        dpg.set_value(item="MusicLoadInfoA",value="(1/5)Loading music! "+yt.title)                                                             
        vids= yt.streams.get_by_itag(251)             
        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA"+str(V),color=(0,255,0))                                                  
        OGGDirectory = r".\ogg"                       
        YTtitle = re.sub(r'[\\/*?:"<>|]',"",yt.title) 
                                                     
        try:                                          
                vids.download(OGGDirectory)           
        except IndexError:                            
                print("No quality found for 251!")    
                vids= yt.streams.get_by_itag(250)     
        else:                                         
                vids.download(OGGDirectory)           
                                                     
        dpg.set_value(item="MusicLoadInfoA",value="(2/5)Loaded! "+yt.title)                                                                    
        time.sleep(0.1)                               
        dpg.set_value(item="MusicLoadInfoA",value="(3/5)Creating file! "+yt.title)                                                             
                                                     
        new_filename = YTtitle+".ogg"
                                                     
        dpg.set_value(item="MusicLoadInfoA",value="(3/5)Created! "+yt.title)                                                                   
        time.sleep(0.1)                               
        dpg.set_value(item="MusicLoadInfoA",value="(4/5)Processing file! "+yt.title)                                                           
                                                     
        default_filename = vids.default_filename
        subprocess.run([                              
                'ffmpeg','-n', '-i',                  
                os.path.join(OGGDirectory, default_filename),                                                                                  
                os.path.join(OGGDirectory, new_filename)                                                                                       
        ])                                            
                                                     
        print(yt.title,' has been downloaded to ', OGGDirectory)                                                                               
        dpg.set_value(item="MusicLoadInfoA",value="(4/5)Cleaning .webm files! "+yt.title)                                                      
        print("Removing all .webm files!")            
                                                     
        for filename in Path(".\ogg").glob("*.webm"): 
                filename.unlink()                     
        dpg.set_value(item="MusicLoadInfoA",value="(5/5)Playing file! "+yt.title)                                                              
        try:                                          
                dpg.set_value(item="MusicPlayerA",value="Currently playing: "+yt.title)                                                        
                dpg.set_value(item="MusicPlayerB",value="Currently playing: "+yt.title)                                                        
                dpg.set_value(item="MusicPlayerC",value="Currently playing: "+yt.title)                                                        
        except:                                       
                print("Once again...")                
                                                     
        try:                                          
                mixer.music.load("./ogg/"+new_filename)                                                                                        
        except error:                                 
                dpg.set_value(item="MusicLoadInfoA",value="(5/5)There was an error [No file found in working directory]! "+yt.title)           
                dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,0,0))                                                 
        else:                                         
                mixer.music.set_volume(Volume)        
                mixer.music.play()                    
                MusicPlaying = True                   
                for q in range(15):                   
                        q = q + 1                     
                        dpg.set_value(item="WhatMusicIsPlaying"+str(q),value="Listening to: "+yt.title)                                        
                        dpg.configure_item(item="WhatMusicIsPlaying"+str(q),tag="WhatMusicIsPlaying"+str(q),color=(0,255,0))                   
                                                     
                time.sleep(2)                         
                dpg.set_value(item="MusicLoadInfoA",value="")                                                                                  


def _MusicStop(sender,app_data):                      
        global MusicPlaying                           
        mixer.music.stop()                            
        dpg.set_value(item="MusicLoadInfoA",value="Stopped!")                                                                                  
        MusicPlaying = False                          
        dpg.set_value(item="MusicPlayerA",value="Currently playing: ")                                                                         
        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,0,0))                                                         
        try:                                          
                dpg.delete_item(item="Thumbnail")     
        except SystemError:                           
                dpg.set_value(item="MusicLoadInfoA",value="Already stopped!")                                                                  
        for q in range(15):                           
                q = q + 1                             
                dpg.set_value(item="WhatMusicIsPlaying"+str(q),value="Listening to: ")                                                         
                dpg.configure_item(item="WhatMusicIsPlaying"+str(q),tag="WhatMusicIsPlaying"+str(q),color=(255,255,255))                       

def _MusicLoop(sender,app_data):                      
        global MusicPlaying                           
        global CurrentTime                            
        global CurrentTime2                           
        global flag1                                  
        if app_data == True and MusicPlaying == True: 
                try:                                  
                        CurrentTime                   
                except NameError:                     
                        print("Current time does not exists")                                                                                  
                if flag1 == False:                    
                        print("-----------------------------")                                                                                 
                        print("Flag 1 FALSE")         
                        try:                          
                                CurrentTime = mixer.music.get_pos()                                                                            
                                print("Current time: ",float(CurrentTime/1000), " seconds")                                                    
                                mixer.music.play(loops=-1,start=float(CurrentTime/1000))                                                       
                        except NameError:             
                                print("Ok")           
                if flag1 == True:                     
                        print("-----------------------------")                                                                                 
                        print("Flag 1 TRUE")          
                        CurrentTime = mixer.music.get_pos()                                                                                    
                        CurrentTime2 = CurrentTime2 + CurrentTime                                                                              
                        print("Time 1 ",float(CurrentTime/1000), " seconds")                                                                   
                        print("Time 2 ",float(CurrentTime2/1000), " seconds")                                                                  
                        print("Current time: ",float(CurrentTime/1000)+float(CurrentTime2/1000), " seconds")                                   
                        mixer.music.play(loops=-1,start=float(CurrentTime2/1000))                                                              
                                                      
                dpg.set_value(item="MusicLoadInfoA",value="Loop added!")                                                                       
                dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(0,255,0))                                                 
                time.sleep(1)                         
                dpg.set_value(item="MusicLoadInfoA",value="")                                                                                  
                dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,255,255))                                             
        elif MusicPlaying == False:                   
                dpg.set_value(item="MusicLoadInfoA",value="No music playing!")                                                                 
                dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,0,0))                                                 
                time.sleep(1)                         
                dpg.set_value(item="MusicLoadInfoA",value="")                                                                                  
                dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,255,255))                                             
        else:                                         
                if flag1 == False:                    
                        print("-----------------------------")                                                                                 
                        print("Loop Deactivated")     
                        flag1 = True                  
                        CurrentTime2 = mixer.music.get_pos()                                                                                   
                        CurrentTime2 = CurrentTime2 + CurrentTime                                                                              
                        print("Time 1 ",float(CurrentTime/1000), " seconds")                                                                   
                        print("Time 2 ",float(CurrentTime2/1000), " seconds")                                                                  
                        print("Current time: ",float(CurrentTime/1000)+float(CurrentTime2/1000), " seconds")                                   
                        mixer.music.play(loops=0,start=float(CurrentTime2/1000))                                                               
                        dpg.set_value(item="MusicLoadInfoA",value="Loop removed!")                                                             
                        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,0,0))                                         
                        time.sleep(1)                 
                        dpg.set_value(item="MusicLoadInfoA",value="")                                                                          
                        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,255,255))                                     
                else:                                 
                        print("-----------------------------")                                                                                 
                        print("FLAG 1 TRUE Loop Deactivated")                                                                                  
                        flag1 = True                  
                        CurrentTime2 = mixer.music.get_pos()                                                                                   
                        CurrentTime2 = CurrentTime2 + CurrentTime                                                                              
                        print("Time 1 ",float(CurrentTime/1000), " seconds")                                                                   
                        print("Time 2 ",float(CurrentTime2/1000), " seconds")                                                                  
                        print("Current time: ",float(CurrentTime/1000)+float(CurrentTime2/1000), " seconds")                                   
                        mixer.music.play(loops=0,start=float(CurrentTime2/1000))                                                               
                        dpg.set_value(item="MusicLoadInfoA",value="Loop removed!")                                                             
                        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,0,0))                                         
                        time.sleep(1)                 
                        dpg.set_value(item="MusicLoadInfoA",value="")                                                                          
                        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,255,255))                                     


def _MusicRewind(sender,app_data,user_data):          
        print(f"sender: {sender}, \t Artist app_data: {app_data}, \t user_data: {user_data}")                                                  
        if 'MusicPlaying' not in globals():           
                dpg.set_value(item="MusicLoadInfoA",value="Nothing is playing!")                                                               
        elif 'MusicPlaying' in globals() and MusicPlaying == True:                                                                             
                mixer.music.rewind()                  
                dpg.set_value(item="MusicLoadInfoA",value="Rewind!")                                                                           
                dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,0,0))                                                 
        else:                                         
                dpg.set_value(item="MusicLoadInfoA",value="There's no music!")                                                                 


def _MusicPause(sender,app_data,user_data):           
        global ToF                                    
        global MusicPlaying                           
        ToF += 1                                      
        ActiveWindow = dpg.get_active_window()        
        V = sender[6:]                                
        print(ActiveWindow)                           
        print("Pause: ",sender," user_data ", user_data(ToF))                                                                                  
        if 'MusicPlaying' not in globals():           
                dpg.set_value(item="MusicLoadInfoA",value="Nothing is playing!")                                                               
        elif 'MusicPlaying' in globals() and MusicPlaying == True:                                                                             
                if (user_data(ToF) % 2) == 0:         
                        mixer.music.pause()           
                        dpg.set_value(item="MusicLoadInfoA",value="Paused!")                                                                   
                        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(255,0,0))                                         
                else:                                 
                        mixer.music.unpause()         
                        dpg.set_value(item="MusicLoadInfoA",value="Unpaused!")                                                                 
                        dpg.configure_item(item="MusicLoadInfoA",tag="MusicLoadInfoA",color=(0,255,0))                                         
        else:                                         
                dpg.set_value(item="MusicLoadInfoA",value="You have stopped the music!")                                                       


def _Volume(sender,app_data):                         
        print("Volume: ",app_data/100)                
        Volume = app_data/100                         
        mixer.music.set_volume(Volume)                
        Get_volume = mixer.music.get_volume()         
        print("Actual Volume: ",Get_volume)           


def _MusicDataCombo(sender,app_data):                 
        global DataSelector                           
        print(f'sender: {sender}, app_data: {app_data}')                                                                                       
        DataSelector = app_data                       
        _MusicPlayerWindowPanel()                     


def _MusicPlayerWindowPanel():
        global JsonLoaded
        global ConnectionDB
        global DataSelector
        global TitleList
        global CircleList
        global AlbumList
        global ArrangementList
        global ReleasedList
        global GenreList
        global OriginalList
        global CharacterList
        global ArtistList
        global _filter_table_id
        global HowMuch
        print(DataSelector)
        JsonDirectory = './Json/'
        JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]
        TitleListM = []
        CircleListM = []
        AlbumListM = []
        CharacterListM = []
        GenreListM = []
        ArrangementListM = []
        ReleasedListM = []
        ArtistListM = []
        URLListM = []
        for index, js in enumerate(JsonFiles):
                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                        JsonText = json.load(JsonFile)
                        Jtitle = JsonText['Music'][0]['root']['Title']
                        Jurl = JsonText['Music'][0]['root']['Options']['Link']
                        Jcircle = JsonText['Music'][0]['root']['Circle']
                        Jalbum = JsonText['Music'][0]['root']['Album']
                        Jarrangement = JsonText['Music'][0]['root']['Arrangement']
                        Jreleased = JsonText['Music'][0]['root']['Released']
                        Jgenre = JsonText['Music'][0]['root']['Genre']
                        Jcharacter = JsonText['Music'][0]['root']['Character']
                        Jartist = JsonText['Music'][0]['root']['Artist']
                        TitleListM.append(Jtitle)
                        CircleListM.append(Jcircle)
                        ArrangementListM.append(Jarrangement)
                        AlbumListM.append(Jalbum)
                        CharacterListM.append(Jcharacter)
                        GenreListM.append(Jgenre)
                        ReleasedListM.append(Jreleased)
                        ArtistListM.append(Jartist)
                        URLListM.append(Jurl)

        for i in range(len(URLListM)):
                d = i
        dpg.show_item("PlaylistTag")
        if DataSelector == "Local data":
                print(DataSelector)
                try:
                        dpg.delete_item(item="CwB")
                except SystemError:
                        print("i would remove it if IT EXISTED")
                if JsonLoaded == True:
                        dpg.set_value(item="IsDataLoaded",value="")
                        dpg.show_item(item="MusicDataSelector")
                        try:
                                dpg.delete_item(item="ReJsonLoad")
                                dpg.delete_item(item="MusicPLoadDBJson")
                        except:
                                print("")
                        DIE = dpg.does_item_exist(item="CwA")
                        if DIE == True:
                                print("Don't do anything else.")
                        else:
                                with dpg.child_window(width=230, height=280,tag="CwA",autosize_x=True,parent="Music_Player_Window",user_data=d):
                                        with dpg.group(horizontal=False,tag="ImageThumbnail"):
                                                print("")
                                                dpg.add_text(label="",tag="MusicPlayerA",user_data=d)
                                        with dpg.group(horizontal=True,tag="GroupA",user_data=d):
                                                dpg.add_button(label="Rewind !",callback=_MusicRewind,tag="RewindA",user_data=d)
                                                dpg.add_button(label="Stop !",callback=_MusicStop,tag="StopA",user_data=d)
                                                dpg.add_button(label="Pause !",callback=_MusicPause,tag="PauseA",user_data=lambda ToF: ToF + 1)
                                                dpg.add_checkbox(label="Loop",tag="LoopMusic", callback=_MusicLoop,user_data=d)
                                        dpg.add_text(label="",tag="MusicLoadInfoA",user_data=d)
                                        dpg.add_slider_int(label="Volume",default_value=10, max_value=100,tag="VolumeA", callback=_Volume,user_data=d)
                                        with dpg.child_window(tag="MusicListTable",autosize_x=True,autosize_y=True,parent="Music_Player_Window",user_data=d):
                                                _filter_table_id = dpg.generate_uuid()
                                                dpg.add_input_text(label="Filter (Title,Circle,Character,Genre...etc)",tag="FilterTable0", user_data=_filter_table_id, callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))
                                                with dpg.tooltip(dpg.last_item()):
                                                        dpg.add_text("Filter usage:\n"
                                                                "  \"\"               display all lines\n"
                                                                "  \"xxx\"         display lines containing \"xxx\"\n"
                                                                "  \"xxx,yyy\"  display lines containing \"xxx\" or \"yyy\"\n"
                                                                "  \"-xxx\"        hide lines containing \"xxx\"")
                                                with dpg.child_window(tag="GroupA2",autosize_x=True,autosize_y=True):
                                                        with dpg.table(header_row=True,resizable=True, no_host_extendX=True, delay_search=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, context_menu_in_body=True,hideable=True, reorderable=True,policy=dpg.mvTable_SizingFixedFit, row_background=True, height=-1,scrollY=True, tag=_filter_table_id) as _filter_table_id:
                                                                dpg.add_table_column(label="Play")
                                                                dpg.add_table_column(label="Title")
                                                                dpg.add_table_column(label="Circle")
                                                                dpg.add_table_column(label="Arrangement")
                                                                dpg.add_table_column(label="Characters")
                                                                dpg.add_table_column(label="Genres")
                                                                dpg.add_table_column(label="Artists")
                                                                dpg.add_table_column(label="Released")
                                                                for i in range(d+1):
                                                                        with dpg.table_row(filter_key=f'{i}'f'{TitleListM[i]}'f'{CircleListM[i]}'f'{AlbumListM[i]}'f'{CharacterListM[i]}'f'{GenreListM[i]}'f'{ArrangementListM[i]}'f'{ArtistListM[i]}'):
                                                                                dpg.add_button(label="Play!",callback=_MusicPlay,tag="PlayT"+str(i),user_data=URLListM[i])
                                                                                with dpg.drag_payload(parent="PlayT"+str(i), drag_data=i, payload_type="ints"):
                                                                                        dpg.add_text(str(TitleListM[i]))
                                                                                dpg.add_text("Title: "+str(TitleListM[i]))
                                                                                dpg.add_text("Circle: "+str(CircleListM[i]))
                                                                                dpg.add_text("Arrangement: "+str(ArrangementListM[i]))
                                                                                dpg.add_text("Character: "+str(CharacterListM[i]))
                                                                                dpg.add_text("Genre: "+str(GenreListM[i]))
                                                                                dpg.add_text("Artist/s: "+str(ArtistListM[i]))
                                                                                dpg.add_text("Released: "+str(ReleasedListM[i]))
                                                        _add_config_options(_filter_table_id, 8, "hideable", "reorderable", "resizable", before=_filter_table_id)
                                        
                else:
                        dpg.set_value(item="IsDataLoaded",value="Load Json from local or DB first!")
        elif DataSelector == "DB data":
                print(DataSelector)
                if ConnectionDB == True:
                        try:
                                dpg.delete_item(item="CwA")
                                dpg.delete_item(item=_filter_table_id)
                                dpg.set_value(item="IsDataLoaded",value="")
                                dpg.show_item(item="MusicDataSelector")
                        except:
                                print("does not exists, yet again")
                        DIE = dpg.does_item_exist(item="CwB")
                        if DIE == True:
                                print("Don't do anything else. 2")
                        else:
                                with dpg.child_window(width=230, height=280,tag="CwB",autosize_x=True,parent="Music_Player_Window",user_data=d):
                                        with dpg.group(horizontal=False,tag="ImageThumbnail"):
                                                print("")
                                                dpg.add_text(label="",tag="MusicPlayerB",user_data=d)
                                        with dpg.group(horizontal=True,tag="GroupB",user_data=d):
                                                dpg.add_button(label="Rewind !",callback=_MusicRewind,tag="RewindB",user_data=d)
                                                dpg.add_button(label="Stop !",callback=_MusicStop,tag="StopB",user_data=d)
                                                dpg.add_button(label="Pause !",callback=_MusicPause,tag="PauseB",user_data=lambda ToF: ToF + 1)
                                                dpg.add_checkbox(label="Loop",tag="LoopMusic", callback=_MusicLoop,user_data=d)
                                        dpg.add_text(label="",tag="MusicLoadInfoA",user_data=d)
                                        dpg.add_slider_int(label="Volume",default_value=10, max_value=100,tag="VolumeA", callback=_Volume,user_data=d)
                                        with dpg.child_window(tag="MusicListTable2",autosize_x=True,autosize_y=True,parent="Music_Player_Window",user_data=d):
                                                _filter_table_id = dpg.generate_uuid()
                                                dpg.add_input_text(label="Filter (Title,Circle,Character,Genre...etc)", user_data=_filter_table_id, callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))
                                                with dpg.tooltip(dpg.last_item()):
                                                        dpg.add_text("Filter usage:\n"
                                                                "  \"\"               display all lines\n"
                                                                "  \"xxx\"         display lines containing \"xxx\"\n"
                                                                "  \"xxx,yyy\"  display lines containing \"xxx\" or \"yyy\"\n"
                                                                "  \"-xxx\"        hide lines containing \"xxx\"")
                                                with dpg.child_window(tag="GroupB2",autosize_x=True,autosize_y=True):
                                                        with dpg.table(header_row=True,resizable=True, no_host_extendX=True, delay_search=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, context_menu_in_body=True,hideable=True, reorderable=True,policy=dpg.mvTable_SizingFixedFit, row_background=True, height=-1,scrollY=True, tag=_filter_table_id) as _filter_table_id:
                                                                dpg.add_table_column(label="Play")
                                                                dpg.add_table_column(label="Title")
                                                                dpg.add_table_column(label="Circle")
                                                                dpg.add_table_column(label="Arrangement")
                                                                dpg.add_table_column(label="Characters")
                                                                dpg.add_table_column(label="Genres")
                                                                dpg.add_table_column(label="Artists")
                                                                dpg.add_table_column(label="Released")
                                                                for i in range(HowMuch):
                                                                        with dpg.table_row(filter_key=f'{i}'f'{str(TitleList[i])[31:-5]}'):
                                                                                dpg.add_button(label="Play!",callback=_MusicPlay,tag="PlayT"+str(i),user_data=URLListM[i])
                                                                                dpg.add_text("Title: "+str(TitleList[i])[31:-5])
                                                                                dpg.add_text("Circle: "+str(CircleList[i])[32:-5])
                                                                                dpg.add_text("Arrangement: "+str(ArrangementList[i])[37:-5])
                                                                                dpg.add_text("Character: "+str(CharacterList[i])[35:-5])
                                                                                dpg.add_text("Genre: "+str(GenreList[i])[31:-5])
                                                                                dpg.add_text("Artist/s: "+str(ArtistList[i])[32:-5])
                                                                                dpg.add_text("Released: "+str(ReleasedList[i])[34:-5])
                else:
                        dpg.set_value(item="MusicLoadInfoA",value="You didn't connect to DB!")
                        dpg.show_item(item="MusicDataSelector")

def _CreatePlaylist(sender,app_data,user_data):
        global TitleListC
        global NewPlaylist
        print("sender: ",sender, " app_data: ",app_data," user_data: ", user_data)
        try:
                PlaylistTitle = dpg.add_input_text(label="Title",tag="PlaylistNewTitle",parent="MusicPlaylists", callback=_GUITitle)
        except:
                print("Title already exists")
        print(PlaylistTitle)
        JsonDirectory = './Json/'
        JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]
        TitleListC = []
        NewPlaylist = []
        for index, js in enumerate(JsonFiles):
                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                        JsonText = json.load(JsonFile)
                        Jtitle = JsonText['Music'][0]['root']['Title']
                        TitleListC.append(Jtitle)

        with dpg.group(parent="MusicPlaylists"):
                dpg.add_text("Add songs:")
                dpg.add_input_text(label="Song", payload_type="ints", width=300, drop_callback=__DropCallback_Set)

        with dpg.table(header_row=True,tag="NewPlaylistTable",parent="MusicPlaylists",resizable=False, no_host_extendX=False, delay_search=False,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, context_menu_in_body=False,policy=dpg.mvTable_SizingStretchProp, row_background=True, height=150,scrollY=True):
                dpg.add_table_column(label="Title")
                dpg.add_table_column(label="Remove")
        with dpg.group(parent="MusicPlaylists",tag="group2",horizontal=True):
                dpg.add_button(label="Save playlist",parent="group2",callback=__SaveDropCallback)
                dpg.add_text(label="",tag="PlaylistInfo",parent="group2")

def __DropCallback_Set(s,a):
        global TitleListC
        global NewPlaylist
        global TitleRow
        global ButtonRemove
        dpg.set_value(s, str(TitleListC[a]))
        try:
                with dpg.table_row(parent="NewPlaylistTable",tag="Row"+str(a)):
                        TitleRow = dpg.add_text("Title: "+str(TitleListC[a]),tag=str(TitleListC[a]))
                        ButtonRemove = dpg.add_button(label="Remove",user_data=a,tag="Remove"+str(a),callback=__RemoveDropCallback)
        except SystemError:
                        dpg.set_value(item="PlaylistInfo",value=str(TitleListC[a])+" has already been added.")

        try:
                set(NewPlaylist.append(TitleRow))
        except:
                dpg.set_value(item="PlaylistInfo",value=str(TitleListC[a])+" has already been added.")

        dpg.set_value(item="PlaylistInfo",value=str(TitleListC[a])+" added.")
        print("New list: ",set(NewPlaylist))

def __RemoveDropCallback(s,a,u):
        global TitleListC
        global NewPlaylist
        global TitleRow
        global ButtonRemove
        
        for List in NewPlaylist:
                print("List: ",List)

        print("Removed: ",TitleListC[u])
        dpg.delete_item(item="Row"+str(u))
        NewPlaylist.remove(str(TitleListC[u]))
        dpg.set_value(item="PlaylistInfo",value=str(TitleListC[u])+" removed.")

def __SaveDropCallback():
        global TitleListC
        global NewPlaylist
        global PlaylistTitle
        cont1 = 0
        cont2 = 0
        cont3 = 0
        PlaylistDir = './Json/Playlist/'
        JsonDirectory = './Json/'
        JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]
        
        for music in set(NewPlaylist):
                cont1 = cont1 + 1
                print("--------")
                print("Id: ",cont1,"Title: ",music)

        try: 
                if cont1 != 0:
                        os.mkdir(path='./Json/Playlist/'+str(PlaylistTitle))
                        PlaylistDir = './Json/Playlist/'+str(PlaylistTitle)
                else:
                        dpg.set_value(item="PlaylistInfo",value="You didn't put any title to the playlist!")
        except: 
                dpg.set_value(item="PlaylistInfo",value="You didn't put any title to the playlist!")
        
        try:
                print("Playlist Title: ",PlaylistTitle)
        except NameError:
                dpg.set_value(item="PlaylistInfo",value="You didn't put any title to the playlist!")
        else:
                if cont1 != 0:
                        print(cont1," songs have been added to the playlist.")
                        dpg.set_value(item="PlaylistInfo",value=str(cont1)+" songs have been added to "+PlaylistTitle)
                else:
                        dpg.set_value(item="PlaylistInfo",value="You haven't introduced anything to the playlist!")

        for titles in TitleListC:
                cont2 = cont2 + 1
                try:
                        print("Titles list: ",NewPlaylist[cont2-1])
                        if titles == NewPlaylist[cont2-1]:
                                print("Match found!")
                                print("id1: ",cont1," title1: ",titles[cont1])
                                print("id2: ",cont2," title2: ",NewPlaylist[cont2-1])
                                try:
                                        shutil.copy(src="./json/TH-"+str(NewPlaylist[cont2-1])+".json",dst=str(PlaylistDir)+"/")
                                except PermissionError:
                                        dpg.set_value(item="PlaylistInfo",value="Permission error, can't operate without permissions!")
                                except FileNotFoundError as error:
                                        print(error)
                except IndexError:
                        print("Not found!")
                else:
                        print("Match found!")
                        print("id1: ",cont1," title1: ",titles[cont1])
                        print("id2: ",cont2," title2: ",NewPlaylist[cont2-1])
                        try:
                                shutil.copy(src="./json/TH-"+str(NewPlaylist[cont2-1])+".json",dst=str(PlaylistDir)+"/")
                        except PermissionError:
                                dpg.set_value(item="PlaylistInfo",value="Permission error, can't operate without permissions!")
                        except FileNotFoundError as error:
                                print(error)


def _PlaylistSelector(s,a,u):
        global _filter_table_id
        global PlaylistItems
        PlaylistItems = os.listdir('./Json/Playlist/')
        print("sender: ",s," app_data: ",a," user_data: ",u)
        if a == 'None':
                JsonDirectory = './Json/'
        else:
                JsonDirectory = './Json/Playlist/'+str(a)
        
        JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]
        TitleListS = []
        CircleListS = []
        AlbumListS = []
        CharacterListS = []
        GenreListS = []
        ArrangementListS = []
        ReleasedListS = []
        ArtistListS = []
        URLListS = []
        for index, js in enumerate(JsonFiles):
                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                        JsonText = json.load(JsonFile)
                        Jtitle = JsonText['Music'][0]['root']['Title']
                        Jurl = JsonText['Music'][0]['root']['Options']['Link']
                        Jcircle = JsonText['Music'][0]['root']['Circle']
                        Jalbum = JsonText['Music'][0]['root']['Album']
                        Jarrangement = JsonText['Music'][0]['root']['Arrangement']
                        Jreleased = JsonText['Music'][0]['root']['Released']
                        Jgenre = JsonText['Music'][0]['root']['Genre']
                        Jcharacter = JsonText['Music'][0]['root']['Character']
                        Jartist = JsonText['Music'][0]['root']['Artist']
                        TitleListS.append(Jtitle)
                        CircleListS.append(Jcircle)
                        ArrangementListS.append(Jarrangement)
                        AlbumListS.append(Jalbum)
                        CharacterListS.append(Jcharacter)
                        GenreListS.append(Jgenre)
                        ReleasedListS.append(Jreleased)
                        ArtistListS.append(Jartist)
                        URLListS.append(Jurl)

        for i in range(len(URLListS)):
                d = i
        if JsonDirectory == 'None':
                try:
                        dpg.delete_item(item="MusicListTable")
                        with dpg.child_window(tag="MusicListTable",autosize_x=True,autosize_y=True,parent="Music_Player_Window",user_data=d):
                                _filter_table_id = dpg.generate_uuid()
                                dpg.add_input_text(label="Filter (Title,Circle,Character,Genre...etc)",tag="FilterTable2", user_data=_filter_table_id, callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))
                                with dpg.tooltip(dpg.last_item()):
                                        dpg.add_text("Filter usage:\n"
                                                "  \"\"               display all lines\n"
                                                "  \"xxx\"         display lines containing \"xxx\"\n"
                                                "  \"xxx,yyy\"  display lines containing \"xxx\" or \"yyy\"\n"
                                                "  \"-xxx\"        hide lines containing \"xxx\"")
                                with dpg.child_window(tag="GroupA2",autosize_x=True,autosize_y=True):
                                        with dpg.table(header_row=True,resizable=True, no_host_extendX=True, delay_search=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, context_menu_in_body=True,hideable=True, reorderable=True,policy=dpg.mvTable_SizingFixedFit, row_background=True, height=-1,scrollY=True, tag=_filter_table_id) as _filter_table_id:
                                                dpg.add_table_column(label="Play")
                                                dpg.add_table_column(label="Title")
                                                dpg.add_table_column(label="Circle")
                                                dpg.add_table_column(label="Arrangement")
                                                dpg.add_table_column(label="Characters")
                                                dpg.add_table_column(label="Genres")
                                                dpg.add_table_column(label="Artists")
                                                dpg.add_table_column(label="Released")
                                                for i in range(d+1):
                                                        with dpg.table_row(filter_key=f'{i}'f'{TitleListS[i]}'f'{CircleListS[i]}'f'{AlbumListS[i]}'f'{CharacterListS[i]}'f'{GenreListS[i]}'f'{ArrangementListS[i]}'f'{ArtistListS[i]}'):
                                                                dpg.add_button(label="Play!",callback=_MusicPlay,tag="PlayT"+str(i),user_data=URLListS[i])
                                                                with dpg.drag_payload(parent="PlayT"+str(i), drag_data=i, payload_type="ints"):
                                                                        dpg.add_text(str(TitleListS[i]))
                                                                dpg.add_text("Title: "+str(TitleListS[i]))
                                                                dpg.add_text("Circle: "+str(CircleListS[i]))
                                                                dpg.add_text("Arrangement: "+str(ArrangementListS[i]))
                                                                dpg.add_text("Character: "+str(CharacterListS[i]))
                                                                dpg.add_text("Genre: "+str(GenreListS[i]))
                                                                dpg.add_text("Artist/s: "+str(ArtistListS[i]))
                                                                dpg.add_text("Released: "+str(ReleasedListS[i]))
                                        _add_config_options(_filter_table_id, 8, "hideable", "reorderable", "resizable", before=_filter_table_id)
                except:
                        print("MusicListTable already exists")
        elif JsonDirectory != 'None':
                dpg.delete_item(item="MusicListTable")
                with dpg.child_window(tag="MusicListTable",autosize_x=True,autosize_y=True,parent="Music_Player_Window",user_data=d):
                        _filter_table_id = dpg.generate_uuid()
                        dpg.add_input_text(label="Filter (Title,Circle,Character,Genre...etc)",tag="FilterTable2", user_data=_filter_table_id, callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))
                        with dpg.tooltip(dpg.last_item()):
                                dpg.add_text("Filter usage:\n"
                                        "  \"\"               display all lines\n"
                                        "  \"xxx\"         display lines containing \"xxx\"\n"
                                        "  \"xxx,yyy\"  display lines containing \"xxx\" or \"yyy\"\n"
                                        "  \"-xxx\"        hide lines containing \"xxx\"")
                        with dpg.child_window(tag="GroupA2",autosize_x=True,autosize_y=True):
                                with dpg.table(header_row=True,resizable=True, no_host_extendX=True, delay_search=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, context_menu_in_body=True,hideable=True, reorderable=True,policy=dpg.mvTable_SizingFixedFit, row_background=True, height=-1,scrollY=True, tag=_filter_table_id) as _filter_table_id:
                                        dpg.add_table_column(label="Play")
                                        dpg.add_table_column(label="Title")
                                        dpg.add_table_column(label="Circle")
                                        dpg.add_table_column(label="Arrangement")
                                        dpg.add_table_column(label="Characters")
                                        dpg.add_table_column(label="Genres")
                                        dpg.add_table_column(label="Artists")
                                        dpg.add_table_column(label="Released")
                                        for i in range(d+1):
                                                with dpg.table_row(filter_key=f'{i}'f'{TitleListS[i]}'f'{CircleListS[i]}'f'{AlbumListS[i]}'f'{CharacterListS[i]}'f'{GenreListS[i]}'f'{ArrangementListS[i]}'f'{ArtistListS[i]}'):
                                                        dpg.add_button(label="Play!",callback=_MusicPlay,tag="PlayT"+str(i),user_data=URLListS[i])
                                                        with dpg.drag_payload(parent="PlayT"+str(i), drag_data=i, payload_type="ints"):
                                                                dpg.add_text(str(TitleListS[i]))
                                                        dpg.add_text("Title: "+str(TitleListS[i]))
                                                        dpg.add_text("Circle: "+str(CircleListS[i]))
                                                        dpg.add_text("Arrangement: "+str(ArrangementListS[i]))
                                                        dpg.add_text("Character: "+str(CharacterListS[i]))
                                                        dpg.add_text("Genre: "+str(GenreListS[i]))
                                                        dpg.add_text("Artist/s: "+str(ArtistListS[i]))
                                                        dpg.add_text("Released: "+str(ReleasedListS[i]))
                                _add_config_options(_filter_table_id, 8, "hideable", "reorderable", "resizable", before=_filter_table_id)

dpg.create_context()

dpg.add_texture_registry(tag="texreg")

with dpg.theme() as ThemeReimu:                       
                                                     
        with dpg.theme_component(dpg.mvAll):          
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 60), category=dpg.mvThemeCat_Core)                                 
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (35, 35, 35, 240), category=dpg.mvThemeCat_Core)                                  
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (35, 35, 35, 10), category=dpg.mvThemeCat_Core)                                    
                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (120, 120, 120, 60), category=dpg.mvThemeCat_Core)                               
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,(205, 0, 0, 160))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab,(205, 0, 0, 160))                                                                
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive,(225, 0, 0, 160))                                                          
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark,(205, 0, 0, 220))                                                                 
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,(205, 0, 0, 160))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,(205, 0, 0, 120))                                                            
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,(205, 0, 0, 160))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,(255,0,0,120))                                                                
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(255,0,0,100))                                                                    
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 9, category=dpg.mvThemeCat_Core)                                             
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 9, category=dpg.mvThemeCat_Core)                                            
                                                     
        with dpg.theme_component(dpg.mvInputInt):     
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 60), category=dpg.mvThemeCat_Core)                                 
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)                                             
                                                     
        with dpg.theme_component(dpg.mvButton):       
                dpg.add_theme_color(dpg.mvThemeCol_Button,(255,0,0,60),category=dpg.mvThemeCat_Core)                                           
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,(255, 0, 0, 160))                                                              
                                                     
        with dpg.theme_component(dpg.mvTab):          
                dpg.add_theme_color(dpg.mvThemeCol_Tab,(255,0,0,60))                                                                           
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(255,0,0,100))                                                                    
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered,(255,0,0,120))                                                                   
                                                     
with dpg.theme() as ThemeCirno:                       
                                                     
        with dpg.theme_component(dpg.mvAll):          
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (100, 170, 255, 60), category=dpg.mvThemeCat_Core)                                 
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 45, 250), category=dpg.mvThemeCat_Core)                                  
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (30, 30, 45, 60), category=dpg.mvThemeCat_Core)                                    
                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (60, 60, 85, 60), category=dpg.mvThemeCat_Core)                                  
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(100, 170, 255, 100))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,(100, 170, 255, 100))                                                           
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,(120, 170, 255, 140))                                                         
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered,(100, 170, 255, 120))                                                  
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive,(100, 170, 255, 160))                                                   
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,(100, 170, 255, 120))                                                         
                dpg.add_theme_color(dpg.mvThemeCol_Button,(100, 170, 255, 60))                                                                 
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,(100, 170, 255, 120))                                                          
                dpg.add_theme_color(dpg.mvThemeCol_Header,(100, 170, 255, 120))                                                                
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg,(70, 120, 185, 250))                                                                
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,(100, 170, 255, 100))                                                         
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt,(100, 170, 245, 20))                                                          
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 9, category=dpg.mvThemeCat_Core)                                             
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 9, category=dpg.mvThemeCat_Core)                                            
                                                     
        with dpg.theme_component(dpg.mvInputInt):     
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (100, 170, 255, 60), category=dpg.mvThemeCat_Core)                                 
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)                                             
                                                     
        with dpg.theme_component(dpg.mvTab):          
                dpg.add_theme_color(dpg.mvThemeCol_Tab,(100, 170, 255, 60))                                                                    
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(100, 170, 255, 100))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered,(100, 170, 255, 120))                                                            
                                                     
with dpg.theme() as ThemeMarisa:                      
                                                     
        with dpg.theme_component(dpg.mvAll):          
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30, 220), category=dpg.mvThemeCat_Core)                                  
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (30, 30, 30, 60), category=dpg.mvThemeCat_Core)                                    
                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (30, 30, 30, 60), category=dpg.mvThemeCat_Core)                                  
                dpg.add_theme_color(dpg.mvThemeCol_Text,(255,255,255,255), category=dpg.mvThemeCat_Core)                                       
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(200, 200, 200, 100))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,(255, 170, 0, 220))                                                           
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,(255, 170, 0, 120))                                                          
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,(255, 170, 0, 160))                                                           
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,(255, 170, 0, 160))                                                           
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,(255, 170, 0, 160))                                                           
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 9, category=dpg.mvThemeCat_Core)                                             
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 9, category=dpg.mvThemeCat_Core)                                            
                                                     
        with dpg.theme_component(dpg.mvInputInt):     
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 210), category=dpg.mvThemeCat_Core)                                
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)                                             
                                                     
        with dpg.theme_component(dpg.mvButton):       
                dpg.add_theme_color(dpg.mvThemeCol_Button,(122, 122, 122,150),category=dpg.mvThemeCat_Core)                                    
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,(255, 170, 0, 150))                                                           
                                                     
        with dpg.theme_component(dpg.mvTab):          
                dpg.add_theme_color(dpg.mvThemeCol_Tab,(122, 122, 122, 140))                                                                   
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(155, 155, 155, 160))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered,(255, 170, 0, 120))                                                              
                                                     
with dpg.theme() as ThemeTenshi:                      
                                                     
        with dpg.theme_component(dpg.mvAll):          
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (245, 245, 245, 255), category=dpg.mvThemeCat_Core)                               
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (245, 245, 245, 250), category=dpg.mvThemeCat_Core)                                
                dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (255, 255, 255, 223), category=dpg.mvThemeCat_Core)                              
                dpg.add_theme_color(dpg.mvThemeCol_Text,(50,50,50,255), category=dpg.mvThemeCat_Core)                                          
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(200, 200, 200, 100))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,(200, 200, 200, 160))                                                         
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed,(111,111,111, 160))                                                        
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,(220, 220, 220, 100))                                                           
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,(190, 190, 190, 140))                                                         
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered,(200, 200, 200, 120))                                                  
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive,(180, 180, 180, 160))                                                   
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg,(180, 180, 180, 250))                                                               
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 9, category=dpg.mvThemeCat_Core)                                             
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200, 200, 200, 220), category=dpg.mvThemeCat_Core)                                
                dpg.add_theme_color(dpg.mvThemeCol_Button,(255, 255, 255,250),category=dpg.mvThemeCat_Core)                                    
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg,(155, 155, 155,200),category=dpg.mvThemeCat_Core)                             
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,(111, 111, 111, 220))                                                         
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,(111, 111, 111, 220))                                                         
                dpg.add_theme_color(dpg.mvThemeCol_Header,(111, 111, 111, 170))                                                                
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt,(111, 111, 111, 50))                                                          
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,(111,111,111, 160))                                                            
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab,(111,111,111, 160))                                                              
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive,(111,111,111, 180))                                                        
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,(111,111,111, 120))                                                          
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,(111,111,111, 160))                                                           
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 9, category=dpg.mvThemeCat_Core)                                            
                                                     
        with dpg.theme_component(dpg.mvTab):          
                dpg.add_theme_color(dpg.mvThemeCol_Tab,(255, 255, 255, 250))                                                                   
                dpg.add_theme_color(dpg.mvThemeCol_TabActive,(200, 200, 200, 220))                                                             
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered,(120, 120, 120, 200))                                                            
                                                     
with dpg.theme() as disableTheme:                     
        with dpg.theme_component(dpg.mvAll, enabled_state=False):                                                                              
                dpg.add_theme_color(dpg.mvThemeCol_Text, (122, 122, 122))                                                                      

dpg.bind_theme(disableTheme)

print(ThemeReimu)
print(ThemeCirno)
print(ThemeMarisa)
print(ThemeTenshi)

configParser = configparser.RawConfigParser()
configParser.read(r'./Config.ini')

def _ThemeSelector(sender, app_data, user_data):                                       
        global SelectedTheme                                                           
        global width                                                                   
        global height                                                                  
        global channels                                                                
        global data                                                                    
        global TextureTagImage                                                         
        global ViewPortWidth                                                           
        print(f"Theme selected: {app_data}")                                           
        SelectedTheme = app_data                                                       
        match app_data:                                                                
                case "Red & White":                                                    
                        dpg.bind_theme(theme=ThemeReimu)                               
                        TextureTagImage = "texture_tag"                                
                        dpg.delete_item("MainImage")                                   
                        with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                                                  
                                print("Viewport in theme selector: ", ViewPortWidth)   
                                dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])                                      
                        configParser['DEFAULT'] = {'defaulttheme':22,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ViewPortResolution,'Filepath':DLpathOp}       
                        with open('Config.ini', 'w') as configfile:                    
                                configParser.write(configfile)                         
                case "Ice Cold":                                                       
                        dpg.bind_theme(theme=ThemeCirno)                               
                        TextureTagImage = "texture_tag_Cr"                             
                        dpg.delete_item("MainImage")                                   
                        with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                                                  
                                print("Viewport in theme selector: ", ViewPortWidth)   
                                dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])                                      
                        configParser['DEFAULT'] = {'defaulttheme':49,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ViewPortResolution,'Filepath':DLpathOp}       
                        with open('Config.ini', 'w') as configfile:                    
                                configParser.write(configfile)                         
                case "Love-Colored Stars":                                             
                        dpg.bind_theme(theme=ThemeMarisa)                              
                        TextureTagImage = "texture_tag_Mr"                             
                        dpg.delete_item("MainImage")                                   
                        with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                                                  
                                print("Viewport in theme selector: ", ViewPortWidth)   
                                dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])                                      
                        configParser['DEFAULT'] = {'defaulttheme':76,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ViewPortResolution,'Filepath':DLpathOp}       
                        with open('Config.ini', 'w') as configfile:                    
                                configParser.write(configfile)                         
                case "Heaven":                                                         
                        dpg.bind_theme(theme=ThemeTenshi)                              
                        TextureTagImage = "texture_tag_Tn"                             
                        dpg.delete_item("MainImage")                                   
                        with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                                                  
                                print("Viewport in theme selector: ", ViewPortWidth)   
                                dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])                                      
                        configParser['DEFAULT'] = {'defaulttheme':100,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ViewPortResolution,'Filepath':DLpathOp}       
                        with open('Config.ini', 'w') as configfile:                    
                                configParser.write(configfile)                         

dpg.create_viewport(title="Touhou Music Database V0.09", width=600, height=700)
dpg.setup_dearpygui()

def _SavedTheme():                            
        global SelectedTheme                  
        global width                          
        global height                         
        global channels                       
        global data                           
        global TextureTagImage                
        global configParser                   
        global ConfigTheme                    
        global MaximizeOp                     
        global FullscreenOp                   
        global ResolutionOp                   
        global DLpathOp                       
        global ViewPortResolution             
        global ViewPortWidth                  
        ConfigTheme = configParser.get('DEFAULT','defaulttheme')                                                                       
        MaximizeOp = configParser.get('DEFAULT','maximize')                                                                            
        FullscreenOp = configParser.get('DEFAULT','fullscreen')                                                                        
        ResolutionOp = configParser.get('DEFAULT','Resolution')                                                                        
        DLpathOp = configParser.get('DEFAULT','filepath')                                                                              
        dpg.bind_theme(theme=int(ConfigTheme))
        print("-----------------------------------------")                                                                             
        print("Config.ini loaded with these parameters!")                                                                              
        print("-----------------------------------------")                                                                             
                                             
        if ConfigTheme == 22 or ConfigTheme == '22':                                                                                   
                SelectedTheme = 22            
                TextureTagImage = "texture_tag"                                                                                        
                dpg.delete_item("MainImage")  
                with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                 
                        dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[ViewPortWidth/6,40])                        
                print("Reimu Theme")          
        elif ConfigTheme == 49 or ConfigTheme == '49':                                                                                 
                TextureTagImage = "texture_tag_Cr"                                                                                     
                dpg.delete_item("MainImage")  
                with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                 
                        dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[ViewPortWidth/6,40])                        
                print("Cirno Theme")          
        elif ConfigTheme == 76 or ConfigTheme == '76':                                                                                 
                TextureTagImage = "texture_tag_Mr"                                                                                     
                dpg.delete_item("MainImage")  
                with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                 
                        dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[ViewPortWidth/6,40])                        
                print("Marisa Theme")         
        elif ConfigTheme == 100 or ConfigTheme == '100':                                                                                 
                TextureTagImage = "texture_tag_Tn"                                                                                     
                dpg.delete_item("MainImage")  
                with dpg.child_window(autosize_x=True,border=False,parent="MainMenu"):                                                 
                        dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[ViewPortWidth/6,40])                        
                print("Tenshi Theme")         
        if str(MaximizeOp) == "yes":          
                dpg.maximize_viewport()       
                dpg.configure_item(texture_tag=TextureTagImage,item="MainImage",parent="MainMenu",pos=[int(GLOBALWidth)/6,40])                       
                dpg.set_value(item="MaximizeCheck",value=True)                                                                         
                dpg.disable_item(item="FullScreenCheck")                                                                               
                dpg.bind_item_theme(item="FullScreenCheck",theme=disableTheme)                                                         
                dpg.hide_item("ScreenResolutionCombo")                                                                                 
        else:                                 
                print("No maximize")          
        if str(FullscreenOp) == "yes":        
                dpg.toggle_viewport_fullscreen()                                                                                       
                dpg.set_value(item="FullScreenCheck",value=True)                                                                       
                dpg.hide_item("ScreenResolutionCombo")                                                                                 
        else:                                 
                print("No fullscreen")        
                dpg.set_value(item="FullScreenCheck",value=False)                                                                      
                                             
        if str(ResolutionOp) == "600x700":    
                ViewPortWidth = 600           
                dpg.set_viewport_width(600)   
                dpg.set_viewport_height(700)  
                ViewPortResolution = "600x700"
                print("Resolution: 600x700")  
                dpg.configure_item(item="ScreenResolutionCombo",default_value="600x700")                                               
        elif str(ResolutionOp) == "900x900":  
                ViewPortWidth = 900           
                dpg.set_viewport_width(900)   
                dpg.set_viewport_height(900)  
                ViewPortResolution = "900x900"
                print("Resolution: 900x900")  
                dpg.configure_item(item="ScreenResolutionCombo",default_value="900x900")                                               
        elif str(ResolutionOp) == "1280x720": 
                ViewPortWidth = 1280          
                dpg.set_viewport_width(1280)  
                dpg.set_viewport_height(720)  
                ViewPortResolution = "1280x720"                                                                                        
                print("Resolution: 1280x720") 
                dpg.configure_item(item="ScreenResolutionCombo",default_value="1280x720")                                              
        print("Current filepath: ",DLpathOp)  
        dpg.set_value(item="CurrentPath",value="Current Path: "+DLpathOp)                                                              

def _PrimaryWindow():
        global ViewPortWidth
        global TextureTagImage
        dpg.hide_item("MainMenu")
        dpg.hide_item("Database_Window")
        dpg.hide_item("Config_Menu")
        dpg.hide_item("Database_Graph_Window")
        dpg.hide_item("Login_Menu")
        dpg.hide_item("Music_Player_Window")
        dpg.show_item("Primary_Window")
        dpg.set_primary_window("MainMenu", False)
        dpg.set_primary_window("Database_Window",False)
        dpg.set_primary_window("Database_Graph_Window",False)
        dpg.set_primary_window("Login_Menu",False)
        dpg.set_primary_window("Music_Player_Window",False)
        dpg.set_primary_window("Primary_Window", True)
        dpg.configure_item(texture_tag=TextureTagImage,item="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])

def _GoHome():
        dpg.hide_item("Primary_Window")
        dpg.hide_item("Database_Window")
        dpg.hide_item("Config_Menu")
        dpg.hide_item("Database_Graph_Window")
        dpg.hide_item("Login_Menu")
        dpg.hide_item("Music_Player_Window")
        dpg.show_item("MainMenu")
        dpg.set_primary_window("Primary_Window", False)
        dpg.set_primary_window("Database_Window",False)
        dpg.set_primary_window("Database_Graph_Window",False)
        dpg.set_primary_window("Login_Menu",False)
        dpg.set_primary_window("Music_Player_Window",False)
        dpg.set_primary_window("MainMenu", True)

def _DatabaseWindow():
        dpg.hide_item("Primary_Window")
        dpg.hide_item("MainMenu")
        dpg.hide_item("Config_Menu")
        dpg.hide_item("Database_Graph_Window")
        dpg.hide_item("Login_Menu")
        dpg.hide_item("Music_Player_Window")
        dpg.show_item("Database_Window")
        dpg.set_primary_window("Primary_Window",False)
        dpg.set_primary_window("MainMenu",False)
        dpg.set_primary_window("Database_Graph_Window",False)
        dpg.set_primary_window("Login_Menu",False)
        dpg.set_primary_window("Music_Player_Window",False)
        dpg.set_primary_window("Database_Window",True)
        _MusicPlayerWindowPanel()

def _ConfigMenu():
        dpg.hide_item("Primary_Window")
        dpg.hide_item("Database_Window")
        dpg.hide_item("MainMenu")
        dpg.hide_item("Database_Graph_Window")
        dpg.hide_item("Login_Menu")
        dpg.hide_item("Music_Player_Window")
        dpg.show_item("Config_Menu")
        dpg.set_primary_window("Primary_Window",False)
        dpg.set_primary_window("MainMenu",False)
        dpg.set_primary_window("Database_Window",False)
        dpg.set_primary_window("Database_Graph_Window",False)
        dpg.set_primary_window("Login_Menu",False)
        dpg.set_primary_window("Config_Menu",True)

def _LoadGraphMenu():
        dpg.hide_item("Database_Window")
        dpg.hide_item("Music_Player_Window")
        dpg.hide_item("Login_Menu")
        dpg.show_item("Database_Graph_Window")
        dpg.set_primary_window("Database_Window",False)
        dpg.set_primary_window("Music_Player_Window",False)
        dpg.set_primary_window("Login_Menu",False)
        dpg.set_primary_window("Database_Graph_Window",True)

def _LoginMenu():
        dpg.hide_item("Primary_Window")
        dpg.hide_item("Database_Window")
        dpg.hide_item("MainMenu")
        dpg.hide_item("Database_Graph_Window")
        dpg.hide_item("Config_Menu")
        dpg.hide_item("Music_Player_Window")
        dpg.show_item("Login_Menu")
        dpg.set_primary_window("Primary_Window",False)
        dpg.set_primary_window("MainMenu",False)
        dpg.set_primary_window("Database_Window",False)
        dpg.set_primary_window("Database_Graph_Window",False)
        dpg.set_primary_window("Config_Menu",False)
        dpg.set_primary_window("Music_Player_Window",False)
        dpg.set_primary_window("Login_Menu",True)

def _MusicPlayerWindow():
        dpg.hide_item("Primary_Window")
        dpg.hide_item("Database_Window")
        dpg.hide_item("MainMenu")
        dpg.hide_item("Database_Graph_Window")
        dpg.hide_item("Config_Menu")
        dpg.hide_item("Login_Menu")
        dpg.show_item("Music_Player_Window")
        dpg.set_primary_window("Primary_Window",False)
        dpg.set_primary_window("MainMenu",False)
        dpg.set_primary_window("Database_Window",False)
        dpg.set_primary_window("Database_Graph_Window",False)
        dpg.set_primary_window("Config_Menu",False)
        dpg.set_primary_window("Login_Menu",False)
        dpg.set_primary_window("Music_Player_Window",True)
        _MusicPlayerWindowPanel()

def _ShowPlaylistMenu():
        try:
                dpg.show_item("MusicPlaylists")
        except:
                print("Stop clicking, it's already created!")

def _CurrentResolution(sender,app_data,user_data):
        global VWidth
        global ViewPortWidth
        global VHeight
        global TextureTagImage
        global MultiView
        VWidth = int(str(app_data[:-3])[1:-2])
        VHeight = int(str(app_data[1:-2])[1:-2])
        if VWidth < 699:
                MultiView = 1.2
                dpg.configure_item(texture_tag=TextureTagImage,item="MainImage",parent="MainMenu",pos=[(VWidth/6),40])
        elif VWidth > 700 and VWidth < 999:
                MultiView = 2
                dpg.configure_item(texture_tag=TextureTagImage,item="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])
        elif VWidth > 1000 and VWidth <1909:
                MultiView = 2.2
                dpg.configure_item(texture_tag=TextureTagImage,item="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])
        elif VWidth > 1910 and VWidth < 1950:
                MultiView = 2.45
                dpg.configure_item(texture_tag=TextureTagImage,item="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])
        elif VWidth > 1951 and VWidth < 2999:
                MultiView = 2.9
                dpg.configure_item(texture_tag=TextureTagImage,item="MainImage",parent="MainMenu",pos=[(VWidth/6)*MultiView,40])
        dpg.set_value(item="CResolution",value=str(VWidth)+"x"+str(VHeight))

def save_callback(music):
    global GUITitle
    global GUICircle
    global GUIAlbum
    global GUIArrangement
    global GUIReleased
    global GUIGenre
    global GUIOriginal
    global GUICharacter
    global GUIArtist
    global GUIVocalist
    global GUILyrics
    global GUIIllustrator
    global GUIVideo
    global GUILink
    GUITitle = str(GUITitle)
    GUICircle = str(GUICircle)
    GUIAlbum = str(GUIAlbum)
    GUIArrangement = str(GUIArrangement)
    GUIReleased = str(GUIReleased)
    GUIGenre = str(GUIGenre)
    GUIOriginal = str(GUIOriginal)
    GUICharacter = str(GUICharacter)
    GUIArtist = str(GUIArtist)
    GUIVocalist = str(GUIVocalist)
    GUIIllustrator = str(GUIIllustrator)
    GUIVideo = str(GUIVideo)
    GUILink = str(GUILink)
    if GUITitle == "" or GUITitle == "37" or not GUITitle or GUITitle == "Unkown Title":
        print("Title is required!")
        dpg.set_value(700,value="Title must have something!")
    elif GUILink == "" or GUILink == "52" or not GUILink or GUILink == "Unkown Link":
        print("URL is required!")
        dpg.set_value(700,value="URL must have something!")
    else:
        print("Title with success!!")
        music = {
                "Music": [
                {
                        "root": {
                        "Title": GUITitle,
                        "Circle": GUICircle,
                        "Album": GUIAlbum,
                        "Arrangement": GUIArrangement,
                        "Released": GUIReleased,
                        "Genre": GUIGenre,
                        "Original": GUIOriginal,
                        "Character": GUICharacter,
                        "Artist": GUIArtist,
                        "Artists": {
                                "Vocal": GUIVocalist,
                                "Lyric": GUILyrics,
                                "Illustration": GUIIllustrator,
                                "Movie": GUIVideo
                        },
                        "Options": {
                                "Link": GUILink
                        }
                        }
                }
                ]
        }
        print("Save Clicked")
        print("Title: ",GUITitle)
        print("Circle: ",GUICircle)
        print("Album: ",GUIAlbum)
        print("Arrangement: ",GUIArrangement)
        print("Released: ",GUIReleased)
        print("Genre: ",GUIGenre)
        print("Original: ",GUIOriginal)
        print("Character: ",GUICharacter)
        print("Artist: ",GUIArtist)
        print("Vocalist: ",GUIVocalist)
        print("Lyrics: ",GUILyrics)
        print("Illustrator: ",GUIIllustrator)
        print("Video: ",GUIVideo)
        print("URL: ",GUILink)
        MusicList = "TH-"+str(GUITitle)+".json"


        json.dump(music, open("./Json/"+MusicList,"w"),indent=4)

        df = pd.read_json(r"./Json/"+MusicList)
        dpg.set_value(701,value="Saved on ./Json/"+MusicList)
        dpg.set_value(700,value="")

def clear_callback():
    dpg.set_value("Unkown Title",value="")
    dpg.set_value("Unkown Circle",value="")
    dpg.set_value("Unkown Album",value="")
    dpg.set_value("Unkown Arrangement",value="")
    dpg.set_value("Unkown Release Date",value="")
    dpg.set_value("Unkown Genre",value="")
    dpg.set_value("Unkown Original",value="")
    dpg.set_value("Unkown Character",value="")
    dpg.set_value("Unkown Artist",value="")
    dpg.set_value("Unkown Vocalist",value="")
    dpg.set_value("Unkown Lyrics",value="")
    dpg.set_value("Unkown Illustrator",value="")
    dpg.set_value("Unkown Video",value="")
    dpg.set_value("Unkown Link",value="")

def _LoadJson(sender,app_data,user_data):
        global JsonFiles
        global JsonDirectory
        global JsonData
        global ConnectionDB
        global table_id
        global DataSelector
        DataSelector = "Local data"
        JsonDirectory = './Json/'
        if JsonLoaded == False:
                JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]
                print(JsonFiles,"\n_loadJson succesful")
        OldJsonTitles = JsonFiles
        for i in range(len(JsonFiles)):
                HowManyOld = i
        if sender == "ReJsonLoad":
                print("Yoo it's me big cheese")
                dpg.delete_item(item="ReJsonLoad")
                dpg.delete_item(item="MusicPLoadDBJson")
        if JsonLoaded == True:
                print("Json has already been loaded!\nAttempting to find new .json files")
                print("OLD JSON TITLES\n---------------------------")
                print(OldJsonTitles)
                NewJsonTitles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')] 
                print("NEW JSON TITLES\n---------------------------")
                print(NewJsonTitles)
                print("Down below")
                s1 = set(OldJsonTitles)
                s2 = set(NewJsonTitles)
                ResultTitles = list(s2.difference(s1))
                print(ResultTitles)
                for titles in range(len(ResultTitles)):
                        HowManyNew = titles
                if ResultTitles:
                        URLList = []
                        print(HowManyNew+1," will be added to the database.")
                        dpg.set_value("TextLocalInfo",str(HowManyNew+1)+" Title/s have been added!")
                        dpg.configure_item(item="TextLocalInfo",tag="TextLocalInfo",parent="DBInfoButtons",color=(0,230,0))
                        JsonData = pd.DataFrame(columns=['Title','Circle','Album','Arrangement','Released','Genre','Original','Character','Artist','Artists','Vocal','Lyric','Illustration','Movie','Options','Link'])
                        with dpg.table(header_row=True, row_background=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, delay_search=True,resizable=True,parent="Database_Window") as table_id:
                                for index, js in enumerate(ResultTitles):
                                        with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                                JsonText = json.load(JsonFile)
                                                Jtitle = JsonText['Music'][0]['root']['Title']
                                                Jcircle = JsonText['Music'][0]['root']['Circle']
                                                Jalbum = JsonText['Music'][0]['root']['Album']
                                                Jarrangement = JsonText['Music'][0]['root']['Arrangement']
                                                Jreleased = JsonText['Music'][0]['root']['Released']
                                                Jgenre = JsonText['Music'][0]['root']['Genre']
                                                Joriginal = JsonText['Music'][0]['root']['Original']
                                                Jcharacter = JsonText['Music'][0]['root']['Character']
                                                Jartist = JsonText['Music'][0]['root']['Artist']
                                                Jartists = JsonText['Music'][0]['root']['Artists']
                                                Jvocal = JsonText['Music'][0]['root']['Artists']['Vocal']
                                                Jlyric = JsonText['Music'][0]['root']['Artists']['Lyric']
                                                Jillustration = JsonText['Music'][0]['root']['Artists']['Illustration']
                                                Jmovie = JsonText['Music'][0]['root']['Artists']['Movie']
                                                Joptions = JsonText['Music'][0]['root']['Options']
                                                Jlink = JsonText['Music'][0]['root']['Options']['Link']
                                                URLList.append(Jlink)
                                                JsonData.loc[index] = [Jtitle,Jcircle,Jalbum,Jarrangement,Jreleased,Jgenre,Joriginal,Jcharacter,Jartist,Jartists,Jvocal,Jlyric,Jillustration,Jmovie,Joptions,Jlink]
                                        for i in range(len(URLList)):
                                                LoadedFile = i
                                        with dpg.tree_node(label=Jtitle,user_data=LoadedFile,parent="Database_Window"):
                                                dpg.add_text("Title: "+Jtitle, bullet=True)
                                                dpg.add_text("Circle: "+Jcircle, bullet=True)
                                                dpg.add_text("Album: "+Jalbum, bullet=True)
                                                dpg.add_text("Arrangement: "+Jarrangement, bullet=True)
                                                dpg.add_text("Released: "+Jreleased, bullet=True)
                                                dpg.add_text("Genre: "+Jgenre, bullet=True)
                                                dpg.add_text("Original: "+Joriginal, bullet=True)
                                                dpg.add_text("Character: "+Jcharacter, bullet=True)
                                                dpg.add_text("Artist: "+Jartist, bullet=True)
                                                with dpg.tree_node(label="Specific Artists"):
                                                        dpg.add_text("Vocalist: "+Jvocal, bullet=True)
                                                        dpg.add_text("Lyric: "+Jlyric, bullet=True)
                                                        dpg.add_text("Illustration: "+Jillustration, bullet=True)
                                                        dpg.add_text("Movie: "+Jmovie, bullet=True)
                                                with dpg.tree_node(label="Options"):
                                                        for i in range(len(URLList)):
                                                                user_data = i
                                                                HowMany = i
                                                        dpg.add_button(label="URL: "+Jlink,user_data=i, small=True,callback=_OpenURL)
                                                        with dpg.tooltip(dpg.last_item()):
                                                                dpg.add_text("Click here to go to the link:\n"+Jlink)
                        NewJsonTitles = []
                else:
                        print(NewJsonTitles,"No new music detected")
                        dpg.set_value(item="TextLocalInfo",value="No new music detected!")
                        dpg.configure_item(item="TextLocalInfo",tag="TextLocalInfo",parent="DBInfoButtons",color=(255,0,0))
        else:
                dpg.hide_item("BlankSpace3")
                dpg.hide_item("BlankSpace4")
                dpg.set_value("TextLocalInfo"," Json files have been loaded!")
                dpg.configure_item(item="LoadJsonButton",label="Reload Local Json",width=110,height=25)
                dpg.configure_item(item="LoadDBJson",label="Load DB files",width=110,height=25)
                dpg.configure_item(item="TextLocalInfo",tag="TextLocalInfo",parent="DBInfoButtons",color=(0,230,0))
                dpg.configure_item(item="DBInfoButtons",tag="DBInfoButtons",horizontal=True)
                dpg.set_value("TextLocalInfo",str(HowManyOld+1)+" Json files have been loaded!")
                Read_Json()

def Read_Json():
        global JsonLoaded
        global LoadJsonButtonClicked
        global DLPath
        global JsonData
        global LoadedFile
        global cluster
        global ConnectionDB
        global table_id
        global Jtitle
        global ToF
        global DataSelector
        DataSelector = "Local data"
        _MusicPlayerWindowPanel()
        URLList = []
        JsonData = pd.DataFrame(columns=['Title','Circle','Album','Arrangement','Released','Genre','Original','Character','Artist','Artists','Vocal','Lyric','Illustration','Movie','Options','Link'])
        if JsonLoaded == False:
                DataFinder = dpg.add_input_text(label="Find anything...",parent="Database_Window",tag="DataFinder", callback=_FilterText)
                with dpg.table(tag="Tablefiles",header_row=True, row_background=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, delay_search=True,resizable=True,parent="Database_Window") as table_id:
                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        Jtitle = JsonText['Music'][0]['root']['Title']
                                        Jcircle = JsonText['Music'][0]['root']['Circle']
                                        Jalbum = JsonText['Music'][0]['root']['Album']
                                        Jarrangement = JsonText['Music'][0]['root']['Arrangement']
                                        Jreleased = JsonText['Music'][0]['root']['Released']
                                        Jgenre = JsonText['Music'][0]['root']['Genre']
                                        Joriginal = JsonText['Music'][0]['root']['Original']
                                        Jcharacter = JsonText['Music'][0]['root']['Character']
                                        Jartist = JsonText['Music'][0]['root']['Artist']
                                        Jartists = JsonText['Music'][0]['root']['Artists']
                                        Jvocal = JsonText['Music'][0]['root']['Artists']['Vocal']
                                        Jlyric = JsonText['Music'][0]['root']['Artists']['Lyric']
                                        Jillustration = JsonText['Music'][0]['root']['Artists']['Illustration']
                                        Jmovie = JsonText['Music'][0]['root']['Artists']['Movie']
                                        Joptions = JsonText['Music'][0]['root']['Options']
                                        Jlink = JsonText['Music'][0]['root']['Options']['Link']
                                        URLList.append(Jlink)
                                        JsonData.loc[index] = [Jtitle,Jcircle,Jalbum,Jarrangement,Jreleased,Jgenre,Joriginal,Jcharacter,Jartist,Jartists,Jvocal,Jlyric,Jillustration,Jmovie,Joptions,Jlink]
                                for i in range(len(URLList)):
                                        LoadedFile = i
                                with dpg.tree_node(label=Jtitle,tag="Musicº"+str(LoadedFile),user_data=LoadedFile,parent="Database_Window"):
                                        with dpg.filter_set(id="filter_id"+str(LoadedFile)):
                                                dpg.add_text("Title: "+Jtitle,filter_key=Jtitle, bullet=True)
                                                dpg.add_text("Circle: "+Jcircle,filter_key=Jcircle, bullet=True)
                                                dpg.add_text("Album: "+Jalbum,filter_key=Jalbum, bullet=True)
                                                dpg.add_text("Arrangement: "+Jarrangement,filter_key=Jarrangement, bullet=True)
                                                dpg.add_text("Released: "+Jreleased,filter_key=Jreleased, bullet=True)
                                                dpg.add_text("Genre: "+Jgenre,filter_key=Jgenre, bullet=True)
                                                dpg.add_text("Original: "+Joriginal,filter_key=Joriginal, bullet=True)
                                                dpg.add_text("Character: "+Jcharacter,filter_key=Jcharacter,bullet=True)
                                                dpg.add_text("Artist: "+Jartist,filter_key=Jartist, bullet=True)
                                                with dpg.tree_node(label="Specific Artists"):
                                                        dpg.add_text("Vocalist: "+Jvocal, bullet=True)
                                                        dpg.add_text("Lyric: "+Jlyric, bullet=True)
                                                        dpg.add_text("Illustration: "+Jillustration, bullet=True)
                                                        dpg.add_text("Movie: "+Jmovie, bullet=True)
                                                with dpg.tree_node(label="Options"):
                                                        for i in range(len(URLList)):
                                                                d = i
                                                        dpg.add_button(label="URL: "+Jlink,user_data=i, small=True,callback=_OpenURL)
                                                        with dpg.tooltip(dpg.last_item()):
                                                                dpg.add_text("Click here to go to the link:\n"+Jlink)
                                                        with dpg.group(horizontal=True):
                                                                dpg.add_button(label='Download video via URL',small=False, callback=_DownloadButton, user_data=d)
                                                                dpg.add_text("Status: ")        
                                                                dpg.add_text(tag="StatusDownloadInfo"+str(d),label="")
                                                        dpg.add_button(label="Play this track !",callback=_MusicPlay,tag="PlayB"+str(d),user_data=URLList[d])


                JsonLoaded = True
                print(JsonData)
                print("Local Json loaded!")
                print(" Json files have been loaded!\n------------------------------------------------------------------------")
                dpg.show_item("DBGraphMenu")
                _MusicPlayerWindowPanel()

def _LoadDBJson(sender):
        global ConnectionDB
        global LoadedFile
        global LinkList
        global table_id
        global Jtitle
        global TitleList
        global CircleList
        global AlbumList
        global ArrangementList
        global ReleasedList
        global GenreList
        global OriginalList
        global CharacterList
        global ArtistList
        global DataSelector
        global HowMuch
        print("Connection: ",ConnectionDB)
        DataSelector = "DB data"
        if JsonLoaded == True:
                dpg.hide_item("Tablefiles")
        if ConnectionDB == True:
                if sender == "MusicPLoadDBJson":
                        print("Yoo it's me big cheese from a DB")
                        dpg.delete_item(item="ReJsonLoad")
                        dpg.delete_item(item="MusicPLoadDBJson")
                dpg.hide_item("BlankSpace3")
                dpg.hide_item("BlankSpace4")
                dpg.configure_item(item="LoadJsonButton",label="Reload DB files",width=110,height=25)
                dpg.configure_item(item="LoadDBJson",label="Load DB files",width=110,height=25)
                dpg.configure_item(item="TextLocalInfo",tag="TextLocalInfo",parent="DBInfoButtons",color=(0,230,0))
                dpg.configure_item(item="DBInfoButtons",tag="DBInfoButtons",horizontal=True)

                db = cluster["THMDBJson"]
                collection = db["THMDBJsonFiles"]

                CollectionTitle = list(collection.find({},{'Music.root.Title':1,'_id':0}))
                CollectionCircle = list(collection.find({},{'Music.root.Circle':1,'_id':0}))
                CollectionAlbum = list(collection.find({},{'Music.root.Album':1,'_id':0}))
                CollectionArrangement = list(collection.find({},{'Music.root.Arrangement':1,'_id':0}))
                CollectionReleased = list(collection.find({},{'Music.root.Released':1,'_id':0}))
                CollectionGenre = list(collection.find({},{'Music.root.Genre':1,'_id':0}))
                CollectionOriginal = list(collection.find({},{'Music.root.Original':1,'_id':0}))
                CollectionCharacter = list(collection.find({},{'Music.root.Character':1,'_id':0}))
                CollectionArtist = list(collection.find({},{'Music.root.Artist':1,'_id':0}))
                CollectionVocal = list(collection.find({},{'Music.root.Artists.Vocal':1,'_id':0}))
                CollectionLyric = list(collection.find({},{'Music.root.Artists.Lyric':1,'_id':0}))
                CollectionIllustration = list(collection.find({},{'Music.root.Artists.Illustration':1,'_id':0}))
                CollectionMovie = list(collection.find({},{'Music.root.Artists.Movie':1,'_id':0}))
                CollectionLink = list(collection.find({},{'Music.root.Options.Link':1,'_id':0}))

                TitleList = []
                CircleList = []
                AlbumList = []
                ArrangementList = []
                ReleasedList = []
                GenreList = []
                OriginalList = []
                CharacterList = []
                ArtistList = []
                VocalList = []
                LyricList = []
                IllustrationList = []
                MovieList = []
                LinkList = []
                
                TitleSTR = [str(c) for c in CollectionTitle]
                CircleSTR = [str(c) for c in CollectionCircle]
                AlbumSTR = [str(c) for c in CollectionAlbum]
                ArrangementSTR = [str(c) for c in CollectionArrangement]
                ReleasedSTR = [str(c) for c in CollectionReleased]
                GenreSTR = [str(c) for c in CollectionGenre]
                OriginalSTR = [str(c) for c in CollectionOriginal]
                CharacterSTR = [str(c) for c in CollectionCharacter]
                ArtistSTR = [str(c) for c in CollectionArtist]
                VocalSTR = [str(c) for c in CollectionVocal]
                LyricSTR = [str(c) for c in CollectionLyric]
                IllustrationSTR = [str(c) for c in CollectionIllustration]
                MovieSTR = [str(c) for c in CollectionMovie]
                LinkSTR = [str(c) for c in CollectionLink]

                for Music in CollectionTitle:
                        TitleSTR = str(Music)
                        TitleSTR = str(TitleSTR[31:])
                        TitleSTR = str(TitleSTR[:-5])
                        TitleList.append(Music)
                
                for Music in CollectionCircle:
                        CircleSTR = str(Music)
                        CircleSTR = str(CircleSTR[32:])
                        CircleSTR = str(CircleSTR[:-5])
                        CircleList.append(Music)

                for Music in CollectionAlbum:
                        AlbumSTR = str(Music)
                        AlbumSTR = str(AlbumSTR[31:])
                        AlbumSTR = str(AlbumSTR[:-5])
                        AlbumList.append(Music)

                for Music in CollectionArrangement:
                        ArrangementSTR = str(Music)
                        ArrangementSTR = str(ArrangementSTR[32:])
                        ArrangementSTR = str(ArrangementSTR[:-5])
                        ArrangementList.append(Music)

                for Music in CollectionReleased:
                        ReleasedSTR = str(Music)
                        ReleasedSTR = str(ReleasedSTR[31:])
                        ReleasedSTR = str(ReleasedSTR[:-5])
                        ReleasedList.append(Music)

                for Music in CollectionGenre:
                        GenreSTR = str(Music)
                        GenreSTR = str(GenreSTR[31:])
                        GenreSTR = str(GenreSTR[:-5])
                        GenreList.append(Music)

                for Music in CollectionOriginal:
                        OriginalSTR = str(Music)
                        OriginalSTR = str(OriginalSTR[31:])
                        OriginalSTR = str(OriginalSTR[:-5])
                        OriginalList.append(Music)

                for Music in CollectionCharacter:
                        CharacterSTR = str(Music)
                        CharacterSTR = str(CharacterSTR[31:])
                        CharacterSTR = str(CharacterSTR[:-5])
                        CharacterList.append(Music)

                for Music in CollectionArtist:
                        ArtistSTR = str(Music)
                        ArtistSTR = str(ArtistSTR[31:])
                        ArtistSTR = str(ArtistSTR[:-5])
                        ArtistList.append(Music)

                for Music in CollectionVocal:
                        VocalSTR = str(Music)
                        VocalSTR = str(VocalSTR[31:])
                        VocalSTR = str(VocalSTR[:-5])
                        VocalList.append(Music)

                for Music in CollectionLyric:
                        LyricSTR = str(Music)
                        LyricSTR = str(LyricSTR[31:])
                        LyricSTR = str(LyricSTR[:-5])
                        LyricList.append(Music)

                for Music in CollectionIllustration:
                        IllustrationSTR = str(Music)
                        IllustrationSTR = str(IllustrationSTR[31:])
                        IllustrationSTR = str(IllustrationSTR[:-5])
                        IllustrationList.append(Music)

                for Music in CollectionMovie:
                        MovieSTR = str(Music)
                        MovieSTR = str(MovieSTR[31:])
                        MovieSTR = str(MovieSTR[:-5])
                        MovieList.append(Music)
                
                for Music in CollectionLink:
                        LinkSTR = str(Music)
                        LinkSTR = str(LinkSTR[31:])
                        LinkSTR = str(LinkSTR[:-5])
                        LinkList.append(Music)
                Minus1 = -1
                for c in range(len(TitleList)):
                        HowMuch = c + 1
                        Minus1 = Minus1 + 1
                        dpg.set_value("TextLocalInfo",str(HowMuch)+" DB files have been loaded!")
                        try:
                                dpg.delete_item(item="Musicº"+str(Minus1))
                        except SystemError:
                                print("Deleting something that doesn't exists....ok...")
                
                print("There is: ",HowMuch," files in the DB")
                try:
                        dpg.hide_item(table_id)
                except NameError:
                        print("Hiding something that doesn't exists....")

                with dpg.table(header_row=True, row_background=True,borders_innerH=True, borders_outerH=True, borders_innerV=True,borders_outerV=True, delay_search=True,resizable=True,parent="Database_Window") as DBTable:
                        for index in range(len(TitleList)):
                                with dpg.tree_node(label=str(TitleList[index])[31:-5],user_data=index,parent="Database_Window"):
                                        dpg.add_text("Title: "+str(TitleList[index])[31:-5], bullet=True)
                                        dpg.add_text("Circle: "+str(CircleList[index])[32:-5], bullet=True)
                                        dpg.add_text("Album: "+str(AlbumList[index])[31:-5], bullet=True)
                                        dpg.add_text("Arrangement: "+str(ArrangementList[index])[37:-5], bullet=True)
                                        dpg.add_text("Released: "+str(ReleasedList[index])[34:-5], bullet=True)
                                        dpg.add_text("Genre: "+str(GenreList[index])[31:-5], bullet=True)
                                        dpg.add_text("Original: "+str(OriginalList[index])[34:-5], bullet=True)
                                        dpg.add_text("Character: "+str(CharacterList[index])[35:-5], bullet=True)
                                        dpg.add_text("Artist: "+str(ArtistList[index])[32:-5], bullet=True)
                                        with dpg.tree_node(label="Specific Artists"):
                                                dpg.add_text("Vocalist: "+str(VocalList[index])[43:-6], bullet=True)
                                                dpg.add_text("Lyric: "+str(LyricList[index])[43:-6], bullet=True)
                                                dpg.add_text("Illustration: "+str(IllustrationList[index])[50:-6], bullet=True)
                                                dpg.add_text("Movie: "+str(MovieList[index])[43:-6], bullet=True)
                                        with dpg.tree_node(label="Options"):
                                                dpg.add_button(label="URL: "+str(LinkList[index])[43:-6],user_data=index, small=True,callback=_OpenURLDB)
                                                with dpg.tooltip(dpg.last_item()):
                                                        dpg.add_text("Click here to go to the link:\n"+str(LinkList[index])[43:-6])
                                                with dpg.group(horizontal=True):
                                                        dpg.add_button(label='Download video via URL',small=False,user_data=index,callback=_DownloadButtonDB)
                                                        dpg.add_text("Status: ")
                                                        dpg.add_text(tag="StatusDownloadInfo"+str(index),label="")
                DBFiles = True
                _MusicPlayerWindowPanel()
        else:
                dpg.set_value("TextLocalInfo","You didn't connect to DB!")
                dpg.set_value("IsDataLoaded","You didn't connect to DB!")
                dpg.configure_item(item="TextLocalInfo",tag="TextLocalInfo",parent="DBInfoButtons",color=(255,0,0))

def _hyperlink(text, address):
    b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
    dpg.bind_item_theme(b, "hyperlinkTheme")

def _FilterText(sender, filter_string):
        global LoadedFile
        for files in range(LoadedFile):
                dpg.set_value("filter_id"+str(files), filter_string)
        print("Filter: ",filter_string)

def _CurrentPath(sender, app_data, user_data):
        global DLPath
        print(f"Sender: ", sender,"App Data: ", app_data,"User_data: ")
        DLPath = app_data
        filePath = DLPath
        print("Current path: ",DLPath)
        dpg.set_value(item="CurrentPath",value="Current Path: "+app_data)
        check(filePath)

def _FileExplorer(sender,app_data,user_data):
        global DLPath
        global filePath
        print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
        DLPath = easygui.diropenbox()
        filePath = DLPath
        print("Current path: ",filePath)
        dpg.set_value(item="CurrentPath",value="Current Path: "+filePath)
        check(filePath)

def check(filePath):
        if os.path.exists(filePath):
                print("Path exists!")
                dpg.set_value(item="IsPathValid",value="Path exists!")
                dpg.configure_item(item="IsPathValid",tag="IsPathValid",color=(0,255,0))
                configParser['DEFAULT'] = {'defaulttheme':ConfigTheme,'Maximize':MaximizeOp,'Fullscreen':FullscreenOp,'Resolution':ResolutionOp,'Filepath':filePath}
                with open('Config.ini', 'w') as configfile:
                        configParser.write(configfile)
                return True
        print("Invalid path")
        dpg.set_value(item="IsPathValid",value="Invalid path!")
        dpg.configure_item(item="IsPathValid",tag="IsPathValid",color=(255,0,0))
        return False


def _DownloadButton(sender, app_data, user_data):
        global DLPath
        JsonDirectory = './Json/'
        JsonFiles = [JsonFile for JsonFile in os.listdir(JsonDirectory) if JsonFile.endswith('.json')]
        URLList = []
        for index, js in enumerate(JsonFiles):
                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                        JsonText = json.load(JsonFile)
                        Jurl = JsonText['Music'][0]['root']['Options']['Link']
                        URLList.append(Jurl)
        print(f"Sender: ", sender,"App Data: ", app_data,"User_data: ",user_data)
        url = URLList[user_data]
        path = DLPath
        dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Downloading!")
        dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,255,51))
        try:
                yt = YouTube(url)
        except URLError:
                print("Url: ",url)
                print("Path: ",path)
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Connection Error most probably an OSError: [WinError 10013]\nif not the URL is invalid!")
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,0,0))
        except OSError:
                time.sleep(1)
                print('Connection Error or Incorrect URL!')
                print("Url: ",url)
                print("Path: ",path)
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Connection Error most probably an OSError: [WinError 10013]\nif not the URL is invalid!")
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,0,0))
        except TypeError:
                print("Url: ",url)
                print("Path: ",path)
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="The URL is invalid!")
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,0,0))
                pass
        except RegexMatchError:
                print("Url: ",url)
                print("Path: ",path)
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Could not find match!\nThe URL is invalid")
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,0,0))

        else:
                print(f"Downloading [{yt.title}] (by {yt.author})")
                print("Url: ",url)
                print("Path: ",path)
                yt.streams.get_highest_resolution().download(path)
                print('Operation completed!')
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Success! Downloaded on path: "+str(path))
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(0,255,0))

def _DownloadButtonDB(sender, app_data, user_data):
        global DLPath
        global LinkList
        print(f"Sender: ", sender,"App Data: ", app_data,"User_data: ",user_data)
        url = str(LinkList[user_data])[43:-6]
        path = DLPath
        dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Downloading!")
        dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,255,51))
        try:
                yt = YouTube(url)
        except OSError:
                print('Connection Error or Incorrect URL!')
                print("Url: ",url)
                print("Path: ",path)
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Connection Error most probably an OSError: [WinError 10013]")
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,0,0))
        except TypeError:
                print("Url: ",url)
                print("Path: ",path)
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="The URL is invalid!")
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,0,0))
        except RegexMatchError:
                print("Url: ",url)
                print("Path: ",path)
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Could not find match!\nThe URL is invalid")
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(255,0,0))
        else:
                print(f"Downloading [{yt.title}] (by {yt.author})")
                print("Url: ",url)
                print("Path: ",path)
                yt.streams.get_highest_resolution().download(path)
                print('Operation completed!')
                dpg.set_value(item="StatusDownloadInfo"+str(user_data),value="Success! Downloaded on path: "+str(path))
                dpg.configure_item(item="StatusDownloadInfo"+str(user_data),tag="StatusDownloadInfo",color=(0,255,0))

def _ComboGraph(sender, app_data, user_data):
        global JsonFiles
        global JsonDirectory
        global JsonText
        print(f"sender: {sender},\t, app_data: {app_data}\tuser_data: {user_data}")
        app_data = str(app_data)

        match app_data:
                case "Circle":
                        print("Circle has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")
                        CircleList = []
                        CircleValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JCircle = JsonText['Music'][0]['root']['Circle']
                                        CircleList.append(JCircle)
                        print("All the Circles:\n------------------------------------------------------------------------\n",CircleList)
                        CircleOccurrences = {}
                        for i in CircleList:
                                if i in CircleOccurrences:
                                        CircleOccurrences[i] += 1
                                else:
                                        CircleOccurrences[i] = 1
                        print("Circle count:\n",CircleOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in CircleOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                CircleValues.append(value)
                        
                        CircleList = list(dict.fromkeys(CircleList))
                        CircleList = [c[0:] + ': ' for c in CircleList]
                        CircleValuesSTR = CircleValues
                        CircleValuesSTR = [str(c) for c in CircleValues]
                        
                        print("\nList of Circles\n------------------------------------------------------------------------\n","ONLY the Circles without duplicates:\n",CircleList,"\n","How many times do they appear:\n",CircleValues)
                        
                        CircleLabels = [i + j for i, j in zip(CircleList,CircleValuesSTR)]
                        print("Final result:\n",CircleLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupCircle",show=True):

                                dpg.add_text("Music Circles Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=500, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=CircleValues, labels=CircleLabels, normalize=True, format="%.0f")
                case "Album":
                        print("Album has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        AlbumList = []
                        AlbumValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JAlbum = JsonText['Music'][0]['root']['Album']
                                        AlbumList.append(JAlbum)
                        print("All the Albums:\n------------------------------------------------------------------------\n",AlbumList)
                        AlbumOccurrences = {}
                        for i in AlbumList:
                                if i in AlbumOccurrences:
                                        AlbumOccurrences[i] += 1
                                else:
                                        AlbumOccurrences[i] = 1
                        print("Album count:\n",AlbumOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in AlbumOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                AlbumValues.append(value)
                        
                        AlbumList = list(dict.fromkeys(AlbumList))
                        AlbumList = [c[0:] + ': ' for c in AlbumList]
                        AlbumValuesSTR = AlbumValues
                        AlbumValuesSTR = [str(c) for c in AlbumValues]
                        
                        print("\nList of Albums\n------------------------------------------------------------------------\n","ONLY the Albums without duplicates:\n",AlbumList,"\n","How many times do they appear:\n",AlbumValues)
                        
                        AlbumLabels = [i + j for i, j in zip(AlbumList,AlbumValuesSTR)]
                        print("Final result:\n",AlbumLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupAlbum",show=True):

                                dpg.add_text("Albums Music Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=550, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=AlbumValues, labels=AlbumLabels, normalize=True, format="%.0f")
                case "Arrangement":
                        print("Arrangement has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        ArrangementList = []
                        ArrangementValues = []
                        
                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JArrangement = JsonText['Music'][0]['root']['Arrangement']
                                        ArrangementList.append(JArrangement)
                        print("All the Arrangements:\n------------------------------------------------------------------------\n",ArrangementList)
                        ArrangementOccurrences = {}
                        for i in ArrangementList:
                                if i in ArrangementOccurrences:
                                        ArrangementOccurrences[i] += 1
                                else:
                                        ArrangementOccurrences[i] = 1
                        print("Arrangement count:\n",ArrangementOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in ArrangementOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                ArrangementValues.append(value)
                        
                        ArrangementList = list(dict.fromkeys(ArrangementList))
                        ArrangementList = [c[0:] + ': ' for c in ArrangementList]
                        ArrangementValuesSTR = ArrangementValues
                        ArrangementValuesSTR = [str(c) for c in ArrangementValues]
                        
                        print("\nList of Arrangements\n------------------------------------------------------------------------\n","ONLY the Arrangements without duplicates:\n",ArrangementList,"\n","How many times do they appear:\n",ArrangementValues)
                        
                        ArrangementLabels = [i + j for i, j in zip(ArrangementList,ArrangementValuesSTR)]
                        print("Final result:\n",ArrangementLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupArrangement",show=True):

                                dpg.add_text("Music Arrangements Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=450, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=ArrangementValues, labels=ArrangementLabels, normalize=True, format="%.0f")
                case "Released":
                        print("Released has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")
                        
                        ReleasedList = []
                        ReleasedValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JReleased = JsonText['Music'][0]['root']['Released']
                                        ReleasedList.append(JReleased)
                        print("All the Released Dates:\n------------------------------------------------------------------------\n",ReleasedList)
                        ReleasedOccurrences = {}
                        for i in ReleasedList:
                                if i in ReleasedOccurrences:
                                        ReleasedOccurrences[i] += 1
                                else:
                                        ReleasedOccurrences[i] = 1
                        print("Released count:\n",ReleasedOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in ReleasedOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                ReleasedValues.append(value)
                        
                        ReleasedList = list(dict.fromkeys(ReleasedList))
                        ReleasedList = [c[0:] + ': ' for c in ReleasedList]
                        ReleasedValuesSTR = ReleasedValues
                        ReleasedValuesSTR = [str(c) for c in ReleasedValues]
                        
                        print("\nList of Releaseds\n------------------------------------------------------------------------\n","ONLY the Releaseds without duplicates:\n",ReleasedList,"\n","How many times do they appear:\n",ReleasedValues)
                        
                        ReleasedLabels = [i + j for i, j in zip(ReleasedList,ReleasedValuesSTR)]
                        print("Final result:\n",ReleasedLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupReleased",show=True):

                                dpg.add_text("Released date Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=400, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=ReleasedValues, labels=ReleasedLabels, normalize=True, format="%.0f")
                case "Genre":
                        print("Genre has been selected")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        GenreList = []
                        GenreValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JGenre = JsonText['Music'][0]['root']['Genre']
                                        GenreList.append(JGenre)
                        print("All the Genres used:\n------------------------------------------------------------------------\n",GenreList)
                        GenreOccurrences = {}
                        for i in GenreList:
                                if i in GenreOccurrences:
                                        GenreOccurrences[i] += 1
                                else:
                                        GenreOccurrences[i] = 1
                        print("Genre count:\n",GenreOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in GenreOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                GenreValues.append(value)
                        
                        GenreList = list(dict.fromkeys(GenreList))
                        GenreList = [c[0:] + ': ' for c in GenreList]
                        GenreValuesSTR = GenreValues
                        GenreValuesSTR = [str(c) for c in GenreValues]
                        
                        print("\nList of genres\n------------------------------------------------------------------------\n","ONLY the genres without duplicates:\n",GenreList,"\n","How many times do they appear:\n",GenreValues)
                        
                        GenreLabels = [i + j for i, j in zip(GenreList,GenreValuesSTR)]
                        print("Final result:\n",GenreLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupGenre",show=True):
                                dpg.add_text("Music Genres Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=400, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=GenreValues, labels=GenreLabels, normalize=True, format="%.0f")
                case "Original":
                        print("Original has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")
                        
                        OriginalList = []
                        OriginalValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JOriginal = JsonText['Music'][0]['root']['Original']
                                        OriginalList.append(JOriginal)                        
                        OriginalOccurrences = {}
                        for i in OriginalList:
                                if i in OriginalOccurrences:
                                        OriginalOccurrences[i] += 1
                                else:
                                        OriginalOccurrences[i] = 1
                        print("Original count:\n",OriginalOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in OriginalOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                OriginalValues.append(value)
                        
                        OriginalList = list(dict.fromkeys(OriginalList))
                        OriginalList = [c[0:] + ': ' for c in OriginalList]
                        OriginalValuesSTR = OriginalValues
                        OriginalValuesSTR = [str(c) for c in OriginalValues]
                        
                        print("\nList of Original themes\n------------------------------------------------------------------------\n","ONLY the Original themes without duplicates:\n",OriginalList,"\n","How many times do they appear:\n",OriginalValues)
                        
                        OriginalLabels = [i + j for i, j in zip(OriginalList,OriginalValuesSTR)]
                        print("Final result:\n",OriginalLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupOriginal",show=True):
                                dpg.add_text("Original theme Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=500, height=300,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=OriginalValues, labels=OriginalLabels, normalize=True, format="%.0f")
                case "Character":
                        print("Character has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        CharacterList = []
                        CharacterValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JCharacter = JsonText['Music'][0]['root']['Character']
                                        CharacterList.append(JCharacter)

                        CharacterOccurrences = {}
                        for i in CharacterList:
                                if i in CharacterOccurrences:
                                        CharacterOccurrences[i] += 1
                                else:
                                        CharacterOccurrences[i] = 1
                        print("Character count:\n",CharacterOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in CharacterOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                CharacterValues.append(value)
                        
                        CharacterList = list(dict.fromkeys(CharacterList))
                        CharacterList = [c[0:] + ': ' for c in CharacterList]
                        CharacterValuesSTR = CharacterValues
                        CharacterValuesSTR = [str(c) for c in CharacterValues]
                        
                        print("\nList of characters\n------------------------------------------------------------------------\n","ONLY the characters without duplicates:\n",CharacterList,"\n","How many times do they appear:\n",CharacterValues)
                        
                        CharacterLabels = [i + j for i, j in zip(CharacterList,CharacterValuesSTR)]
                        print("Final result:\n",CharacterLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupCharacter",show=True):
                                dpg.add_text("Characters Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=400, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=CharacterValues, labels=CharacterLabels, normalize=True, format="%.0f")

                case "Artist":
                        print("Artist has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        ArtistList = []
                        ArtistValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JArtist = JsonText['Music'][0]['root']['Artist']
                                        ArtistList.append(JArtist)
                        print("All the Artists:\n------------------------------------------------------------------------\n",ArtistList)
                        ArtistOccurrences = {}
                        for i in ArtistList:
                                if i in ArtistOccurrences:
                                        ArtistOccurrences[i] += 1
                                else:
                                        ArtistOccurrences[i] = 1
                        print("Artists count:\n",ArtistOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in ArtistOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                ArtistValues.append(value)
                        
                        ArtistList = list(dict.fromkeys(ArtistList))
                        ArtistList = [c[0:] + ': ' for c in ArtistList]
                        ArtistValuesSTR = ArtistValues
                        ArtistValuesSTR = [str(c) for c in ArtistValues]
                        
                        print("\nList of artists\n------------------------------------------------------------------------\n","ONLY the artists without duplicates:\n",ArtistList,"\n","How many times do they appear:\n",ArtistValues)
                        
                        ArtistLabels = [i + j for i, j in zip(ArtistList,ArtistValuesSTR)]
                        print("Final result:\n",ArtistLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupArtists",show=True):
                                dpg.add_text("Music Artists Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=400, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=ArtistValues, labels=ArtistLabels, normalize=True, format="%.0f")
                case "Vocalist":
                        print("Vocalist has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        VocalistList = []
                        VocalistValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JVocalist = JsonText['Music'][0]['root']['Artists']['Vocal']
                                        VocalistList.append(JVocalist)
                        print("All the Vocalists:\n------------------------------------------------------------------------\n",VocalistList)
                        VocalistOccurrences = {}
                        for i in VocalistList:
                                if i in VocalistOccurrences:
                                        VocalistOccurrences[i] += 1
                                else:
                                        VocalistOccurrences[i] = 1
                        print("Vocalist count:\n",VocalistOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in VocalistOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                VocalistValues.append(value)
                        
                        VocalistList = list(dict.fromkeys(VocalistList))
                        VocalistList = [c[0:] + ': ' for c in VocalistList]
                        VocalistValuesSTR = VocalistValues
                        VocalistValuesSTR = [str(c) for c in VocalistValues]
                        
                        print("\nList of Vocalists\n------------------------------------------------------------------------\n","ONLY the Vocalists without duplicates:\n",VocalistList,"\n","How many times do they appear:\n",VocalistValues)
                        
                        VocalistLabels = [i + j for i, j in zip(VocalistList,VocalistValuesSTR)]
                        print("Final result:\n",VocalistLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupVocalist",show=True):
                                dpg.add_text("Vocalists Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=500, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=VocalistValues, labels=VocalistLabels, normalize=True, format="%.0f")
                case "Lyric":
                        print("Lyric has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        LyricList = []
                        LyricValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JLyric = JsonText['Music'][0]['root']['Artists']['Lyric']
                                        LyricList.append(JLyric)
                        print("All the Lyrics:\n------------------------------------------------------------------------\n",LyricList)
                        LyricOccurrences = {}
                        for i in LyricList:
                                if i in LyricOccurrences:
                                        LyricOccurrences[i] += 1
                                else:
                                        LyricOccurrences[i] = 1
                        print("Lyric count:\n",LyricOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in LyricOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                LyricValues.append(value)
                        
                        LyricList = list(dict.fromkeys(LyricList))
                        LyricList = [c[0:] + ': ' for c in LyricList]
                        LyricValuesSTR = LyricValues
                        LyricValuesSTR = [str(c) for c in LyricValues]
                        
                        print("\nList of Lyrics\n------------------------------------------------------------------------\n","ONLY the Lyrics without duplicates:\n",LyricList,"\n","How many times do they appear:\n",LyricValues)
                        
                        LyricLabels = [i + j for i, j in zip(LyricList,LyricValuesSTR)]
                        print("Final result:\n",LyricLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupLyric",show=True):
                                dpg.add_text("Music Lyrics Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=400, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=LyricValues, labels=LyricLabels, normalize=True, format="%.0f")
                case "Illustrator":
                        print("Illustrator has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        VocalistActive = dpg.does_alias_exist("GroupVocalist")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        VideoActive = dpg.does_alias_exist("GroupVideo")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif VocalistActive == True:
                                dpg.delete_item("GroupVocalist")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif VideoActive == True:
                                dpg.delete_item("GroupVideo")

                        IllustratorList = []
                        IllustratorValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JIllustrator = JsonText['Music'][0]['root']['Artists']['Illustration']
                                        IllustratorList.append(JIllustrator)
                        print("All the Illustrators:\n------------------------------------------------------------------------\n",IllustratorList)
                        IllustratorOccurrences = {}
                        for i in IllustratorList:
                                if i in IllustratorOccurrences:
                                        IllustratorOccurrences[i] += 1
                                else:
                                        IllustratorOccurrences[i] = 1
                        print("Illustrator count:\n",IllustratorOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in IllustratorOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                IllustratorValues.append(value)
                        
                        IllustratorList = list(dict.fromkeys(IllustratorList))
                        IllustratorList = [c[0:] + ': ' for c in IllustratorList]
                        IllustratorValuesSTR = IllustratorValues
                        IllustratorValuesSTR = [str(c) for c in IllustratorValues]
                        
                        print("\nList of Illustrators\n------------------------------------------------------------------------\n","ONLY the Illustrators without duplicates:\n",IllustratorList,"\n","How many times do they appear:\n",IllustratorValues)
                        
                        IllustratorLabels = [i + j for i, j in zip(IllustratorList,IllustratorValuesSTR)]
                        print("Final result:\n",IllustratorLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupIllustrator",show=True):
                                dpg.add_text("Illustrators Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=400, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=IllustratorValues, labels=IllustratorLabels, normalize=True, format="%.0f")
                case "Video":
                        print("Video has been selected")
                        GenreActive = dpg.does_alias_exist("GroupGenre")
                        OriginalActive = dpg.does_alias_exist("GroupOriginal")
                        CharacterActive = dpg.does_alias_exist("GroupCharacter")
                        CircleActive = dpg.does_alias_exist("GroupCircle")
                        AlbumActive = dpg.does_alias_exist("GroupAlbum")
                        ArrangementActive = dpg.does_alias_exist("GroupArrangement")
                        ReleasedActive = dpg.does_alias_exist("GroupReleased")
                        ArtistActive = dpg.does_alias_exist("GroupArtists")
                        LyricActive = dpg.does_alias_exist("GroupLyric")
                        IllustratorActive = dpg.does_alias_exist("GroupIllustrator")
                        if GenreActive == True:
                                dpg.delete_item("GroupGenre")
                        elif OriginalActive == True:
                                dpg.delete_item("GroupOriginal")
                        elif CharacterActive == True:
                                dpg.delete_item("GroupCharacter")
                        elif CircleActive == True:
                                dpg.delete_item("GroupCircle")
                        elif AlbumActive == True:
                                dpg.delete_item("GroupAlbum")
                        elif ArrangementActive == True:
                                dpg.delete_item("GroupArrangement")
                        elif ReleasedActive == True:
                                dpg.delete_item("GroupReleased")
                        elif ArtistActive == True:
                                dpg.delete_item("GroupArtists")
                        elif LyricActive == True:
                                dpg.delete_item("GroupLyric")
                        elif IllustratorActive == True:
                                dpg.delete_item("GroupIllustrator")

                        VideoList = []
                        VideoValues = []

                        for index, js in enumerate(JsonFiles):
                                with open(os.path.join(JsonDirectory, js),encoding="utf-8") as JsonFile:
                                        JsonText = json.load(JsonFile)
                                        JVideo = JsonText['Music'][0]['root']['Artists']['Movie']
                                        VideoList.append(JVideo)
                        print("All the Video producers:\n------------------------------------------------------------------------\n",VideoList)
                        VideoOccurrences = {}
                        for i in VideoList:
                                if i in VideoOccurrences:
                                        VideoOccurrences[i] += 1
                                else:
                                        VideoOccurrences[i] = 1
                        print("Video count:\n",VideoOccurrences,"\n------------------------------------------------------------------------")
                        for key,value in VideoOccurrences.items():
                                print("The Occurrence of |{0}| in the files is: {1}".format(key, value))
                                VideoValues.append(value)
                        
                        VideoList = list(dict.fromkeys(VideoList))
                        VideoList = [c[0:] + ': ' for c in VideoList]
                        VideoValuesSTR = VideoValues
                        VideoValuesSTR = [str(c) for c in VideoValues]
                        
                        print("\nList of Videos\n------------------------------------------------------------------------\n","ONLY the Videos without duplicates:\n",VideoList,"\n","How many times do they appear:\n",VideoValues)
                        
                        VideoLabels = [i + j for i, j in zip(VideoList,VideoValuesSTR)]
                        print("Final result:\n",VideoLabels)
                        with dpg.group(horizontal=False,parent="Database_Graph_Window",tag="GroupVideo",show=True):
                                dpg.add_text("Videos Graph")
                                with dpg.plot(no_title=True, no_mouse_pos=True, width=400, height=250,tag="PlotChart"):
                                        dpg.add_plot_legend(outside=True)
                                        dpg.add_plot_axis(dpg.mvXAxis, label="",parent="PlotChart", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                                        dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                                                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                                                dpg.add_pie_series(0.5, 0.5, 0.5, values=VideoValues, labels=VideoLabels, normalize=True, format="%.0f")
                case _:
                        print("What...")

fontDir = "./Fonts/rounded-mgenplus-2cp-regular.ttf"
with dpg.font_registry():
    with dpg.font(fontDir, 17) as font1:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Thai)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
    default_font = dpg.add_font(fontDir, 17)

width, height, channels, data = dpg.load_image("./src/TohoMusicDatabase.png")
width, height, channels, data2 = dpg.load_image("./src/TohoMusicDatabaseCr.png")
width, height, channels, data3 = dpg.load_image("./src/TohoMusicDatabaseMr.png")
width, height, channels, data4 = dpg.load_image("./src/TohoMusicDatabaseTn.png")

with dpg.texture_registry(show=False):
    dpg.add_static_texture(width, height, data, tag="texture_tag")
    dpg.add_static_texture(width, height, data2, tag="texture_tag_Cr")
    dpg.add_static_texture(width, height, data3, tag="texture_tag_Mr")
    dpg.add_static_texture(width, height, data4, tag="texture_tag_Tn")

with dpg.window(tag="MainMenu"):
        Viewport = dpg.set_viewport_resize_callback(callback=_CurrentResolution)
        ViewPortWidth = dpg.get_viewport_width()
        ViewPortHeight = dpg.get_viewport_height()
        with dpg.child_window(autosize_x=True,border=False):
                dpg.add_image(texture_tag=TextureTagImage,tag="MainImage",parent="MainMenu",pos=[0,40])
        with dpg.menu_bar():
                with dpg.menu(label="Home"):
                        dpg.add_menu_item(label="Go Home",callback=_GoHome)
                        with dpg.menu(label="About"):
                                dpg.add_text("The THMD or TouHou Music Database is a small but appasionate proyect\nthat started as a small script where you could input the information\nof your favorite remixes/songs/musics that are about Touhou.\n\nThe more i developed this proyect the more i felt i had to improve\nso it was some sort of feedback loop of error and succes eventually\nhitting a point of needing a GUI.\nthe GUI library in question is DearPyGUI and it's very genuine and easy to use.\n\nI love DearPyGUI for it's simplicity yet it's versatility.\nThis was written in V0.01")
                                with dpg.tooltip(dpg.last_item()):
                                        dpg.add_text("(東方) Music Database")
                with dpg.menu(label="Login"):
                        dpg.add_button(label="Login menu",callback=_LoginMenu)
                        dpg.add_text("Logged as: ")
                        dpg.add_text(UserNameL,tag="LoginInfo1")
                with dpg.menu(label="Music Player"):
                        dpg.add_menu_item(label="Go to music player",callback=_MusicPlayerWindow)
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying3")
                dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying4")
        with dpg.child_window(width=-1, height=95, pos=[10,200],border=False):
                layout_demo_table = dpg.generate_uuid()
                with dpg.table(tag=layout_demo_table, header_row=False, borders_innerH=False, borders_outerH=False, borders_innerV=False, borders_outerV=False) as layout_demo_table:
                        dpg.add_table_column()
                        dpg.add_table_column()
                        dpg.add_table_column()
                        with dpg.table_row():
                                dpg.add_button(label="Insert Music", width=-1 , height=55, callback=_PrimaryWindow)
                                dpg.add_button(label="Music Database", width=-1 , height=55, callback=_DatabaseWindow)
                                dpg.add_button(label="Config", width=-1 ,height=55, callback=_ConfigMenu)
                _add_config_options(layout_demo_table, 3, before=layout_demo_table)
        with dpg.child_window(width=300, height=300,autosize_x=True,pos=[10,300]):
                with dpg.tab_bar():
                        with dpg.tab(label="ChangeLog"):
                                dpg.add_text("This is the ChangeLog tab!")
                                dpg.add_text("Changes will be posted here in tabs!")
                                with dpg.group(horizontal=True):
                                        dpg.add_text("Current version:")
                                        dpg.add_text("V0.09",tag="V009",color=(250,255,50))
                                dpg.add_text("Released: 10/06/2022")
                                with dpg.group(horizontal=True):
                                        dpg.add_text("This was made by")
                                        _hyperlink("Fumo Friday Official", "https://twitter.com/friday_fumo")
                        with dpg.tab(label="V0.09"):
                                dpg.add_text("Added themes! Now there's 4 themes to choose!")
                                dpg.add_text("Added music player!")
                                dpg.add_text("Released: 10/06/2022")
                        with dpg.tab(label="V0.08"):
                                dpg.add_text("Finally created a DB for this software!")
                                dpg.add_text("Added login to DB!")
                                dpg.add_text("Directoy explorer for more easy access!")
                                dpg.add_text("Released: 03/06/2022")
                        with dpg.tab(label="V0.07"):
                                dpg.add_text("Download music with URL!")
                                dpg.add_text("Fullscreen added")
                                dpg.add_text("Removed save file selector")
                                dpg.add_text("Released: 30/05/2022")
                        with dpg.tab(label="V0.06"):
                                dpg.add_text("Load graphs button!")
                                dpg.add_text("Now with more graphs with data!")
                                dpg.add_text("Released: 27/05/2022")
                        with dpg.tab(label="V0.05"):
                                dpg.add_text("Improved Load Json button!")
                                dpg.add_text("Improved overall database info!")
                                dpg.add_text("Released: 23/05/2022") 
                        with dpg.tab(label="V0.04"):
                                dpg.add_text("Config button added and working!")
                                dpg.add_text("Different resolutions!")
                                dpg.add_text("New icon!")       
                                dpg.add_text("Released: 22/05/2022") 
                        with dpg.tab(label="V0.03"):
                                dpg.add_text("Now you can visit any song by click it's URL!")
                                dpg.add_text("Music table into tree node!")
                                dpg.add_text("Released: 21/05/2022")
                        with dpg.tab(label="V0.02"):
                                dpg.add_text("A new icon look!")
                                dpg.add_text("Json info into tables!")
                                dpg.add_text("Released: 18/05/2022")
                        with dpg.tab(label="V0.01"):
                                dpg.add_text("Added GUI!")
                                dpg.add_text("Awesome buttons!")
                                dpg.add_text("Able to load json files!")
                                dpg.add_text("Released: 17/05/2022")
        with dpg.child_window(width=-1, height=50,autosize_x=True, border=False):
                Exit = dpg.generate_uuid()
                with dpg.table(tag=Exit, header_row=False, borders_innerH=False, borders_outerH=False, borders_innerV=False, borders_outerV=False) as Exit:
                                dpg.add_table_column()
                                dpg.add_table_column()
                                dpg.add_table_column()
                                with dpg.table_row():
                                        dpg.add_text(label=" ")
                                        dpg.add_button(label="Exit", width=150 , callback=lambda:dpg.stop_dearpygui())
                                        dpg.add_text(label=" ")
                        
                _add_config_options(Exit, 3, before=Exit)
        with dpg.window(tag="Primary_Window",show=False):
                with dpg.menu_bar():
                        with dpg.menu(label="Home"):
                                dpg.add_menu_item(label="Go Home",callback=_GoHome)
                                with dpg.menu(label="About"):
                                        dpg.add_text("The THMD or TouHou Music Database is a small but appasionate proyect\nthat started as a small script where you could input the information\nof your favorite remixes/songs/musics that are about Touhou.\n\nThe more i developed this proyect the more i felt i had to improve\nso it was some sort of feedback loop of error and succes eventually\nhitting a point of needing a GUI.\nthe GUI library in question is DearPyGUI and it's very genuine and easy to use.\n\nI love DearPyGUI for it's simplicity yet it's versatility.\nThis was written in V0.01")
                                        with dpg.tooltip(dpg.last_item()):
                                                dpg.add_text("(東方) Music Database")
                        with dpg.menu(label="Login"):
                                dpg.add_button(label="Login menu",callback=_LoginMenu)
                                dpg.add_text("Logged as: ")
                                dpg.add_text(UserNameL,tag="LoginInfo2")
                        with dpg.menu(label="Music Player"):
                                dpg.add_menu_item(label="Go to music player",callback=_MusicPlayerWindow)
                                dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying5")
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying6")
                dpg.add_text("Put as much valid data as possible", color=(255,0,0))
                dpg.add_text("",tag=700,color=(255,0,0))
                dpg.add_text("",tag=701,color=(0,230,0))
                with dpg.child_window(width=500, height=515):
                        dpg.add_text("{*} Text fields are required")
                        dpg.add_text("If you can't find valid/verified data type none.\nIf you know it exists but can't find the name for it don't type anything")
                        GUITitle = dpg.add_input_text(label="Title {*}",tag="Unkown Title", callback=_GUITitle)
                        GUICircle = dpg.add_input_text(label="Circle",tag="Unkown Circle", callback=_GUICircle)
                        GUIAlbum = dpg.add_input_text(label="Album",tag="Unkown Album",callback=_GUIAlbum)
                        GUIArrangement = dpg.add_input_text(label="Arrangement",tag="Unkown Arrangement",callback=_GUIArrangement)
                        GUIReleased = dpg.add_input_text(label="Released",tag="Unkown Release Date",callback=_GUIReleased)
                        GUIGenre = dpg.add_input_text(label="Genre",tag="Unkown Genre",callback=_GUIGenre)
                        GUIOriginal = dpg.add_input_text(label="Original",tag="Unkown Original",callback=_GUIOriginal)
                        GUICharacter = dpg.add_input_text(label="Character",tag="Unkown Character",callback=_GUICharacter)
                        GUIArtist = dpg.add_input_text(label="Artist",tag="Unkown Artist",callback=_GUIArtist)
                        GUIVocalist = dpg.add_input_text(label="Vocalist",tag="Unkown Vocalist",callback=_GUIVocalist)
                        GUILyrics = dpg.add_input_text(label="Lyrics",tag="Unkown Lyrics",callback=_GUILyrics)
                        GUIIllustrator = dpg.add_input_text(label="Illustrator",tag="Unkown Illustrator",callback=_GUIIllustrator)
                        GUIVideo = dpg.add_input_text(label="Video",tag="Unkown Video",callback=_GUIVideo)
                        GUILink = dpg.add_input_text(label="Link {*}",tag="Unkown Link",callback=_GUILink)
                dpg.bind_font(font1)
                with dpg.group(horizontal=True):
                        dpg.add_button(label="Save", callback=save_callback)
                        dpg.add_button(label="Clear all", callback=clear_callback)
        with dpg.window(tag="Database_Window",show=False):
                with dpg.menu_bar():
                        with dpg.menu(label="Home"):
                                dpg.add_menu_item(label="Go Home",callback=_GoHome)
                                with dpg.menu(label="About"):
                                        dpg.add_text("The THMD or TouHou Music Database is a small but appasionate proyect\nthat started as a small script where you could input the information\nof your favorite remixes/songs/musics that are about Touhou.\n\nThe more i developed this proyect the more i felt i had to improve\nso it was some sort of feedback loop of error and succes eventually\nhitting a point of needing a GUI.\nthe GUI library in question is DearPyGUI and it's very genuine and easy to use.\n\nI love DearPyGUI for it's simplicity yet it's versatility.\nThis was written in V0.01")
                                        with dpg.tooltip(dpg.last_item()):
                                                dpg.add_text("(東方) Music Database")
                        with dpg.menu(label="Login"):
                                dpg.add_button(label="Login menu",callback=_LoginMenu)
                                dpg.add_text("Logged as: ")
                                dpg.add_text(UserNameL,tag="LoginInfo3")
                        with dpg.menu(label="Music Player"):
                                dpg.add_menu_item(label="Go to music player",callback=_MusicPlayerWindow)
                                dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying2")
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying1")
                dpg.add_text("Welcome to the Music Database")
                with dpg.group(horizontal=False,tag="DBInfoButtons"):
                        dpg.add_button(label="Load local Json",width=-1,height=100,tag="LoadJsonButton", callback=_LoadJson)
                        dpg.add_text("",tag="BlankSpace3")
                        dpg.add_text("",tag="BlankSpace4")
                        dpg.add_button(label="Load DB files",width=-1,height=100,tag="LoadDBJson",callback=_LoadDBJson)
                        LoadJsonButtonClicked = dpg.is_item_clicked(item="LoadJsonButton")
                        dpg.add_text("Json data hasn't been loaded!",tag="TextLocalInfo",color=(255,0,0))
                        dpg.add_button(label="Graph Menu",tag="DBGraphMenu",show=False, callback=_LoadGraphMenu)
        with dpg.window(tag="Database_Graph_Window",show=False):
                with dpg.menu_bar():
                        with dpg.menu(label="Home"):
                                dpg.add_menu_item(label="Go Home",callback=_GoHome)
                                with dpg.menu(label="About"):
                                        dpg.add_text("The THMD or TouHou Music Database is a small but appasionate proyect\nthat started as a small script where you could input the information\nof your favorite remixes/songs/musics that are about Touhou.\n\nThe more i developed this proyect the more i felt i had to improve\nso it was some sort of feedback loop of error and succes eventually\nhitting a point of needing a GUI.\nthe GUI library in question is DearPyGUI and it's very genuine and easy to use.\n\nI love DearPyGUI for it's simplicity yet it's versatility.\nThis was written in V0.01")
                                        with dpg.tooltip(dpg.last_item()):
                                                dpg.add_text("(東方) Music Database")
                        with dpg.menu(label="Login"):
                                dpg.add_button(label="Login menu",callback=_LoginMenu)
                                dpg.add_text("Logged as: ")
                                dpg.add_text(UserNameL,tag="LoginInfo4")
                        with dpg.menu(label="Music Player"):
                                dpg.add_menu_item(label="Go to music player",callback=_MusicPlayerWindow)
                                dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying7")
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying8")
                with dpg.group(horizontal=True,tag="DBGraphButtons"):
                        dpg.add_text("Graphs Selector",tag="GraphMenu")
                        items = ("Circle","Album","Arrangement","Released","Genre","Original","Character","Artist","Vocalist","Lyric","Illustrator","Video")
                GraphCombo = dpg.add_combo(items, label="Music Data", height_mode=dpg.mvComboHeight_Regular,callback=_ComboGraph)
        with dpg.window(tag="Config_Menu",show=False):
                with dpg.menu_bar():
                        with dpg.menu(label="Home"):
                                dpg.add_menu_item(label="Go Home",callback=_GoHome)
                                with dpg.menu(label="About"):
                                        dpg.add_text("The THMD or TouHou Music Database is a small but appasionate proyect\nthat started as a small script where you could input the information\nof your favorite remixes/songs/musics that are about Touhou.\n\nThe more i developed this proyect the more i felt i had to improve\nso it was some sort of feedback loop of error and succes eventually\nhitting a point of needing a GUI.\nthe GUI library in question is DearPyGUI and it's very genuine and easy to use.\n\nI love DearPyGUI for it's simplicity yet it's versatility.\nThis was written in V0.01")
                                        with dpg.tooltip(dpg.last_item()):
                                                dpg.add_text("(東方) Music Database")                        
                        with dpg.menu(label="Login"):
                                dpg.add_button(label="Login menu",callback=_LoginMenu)
                                dpg.add_text("Logged as: ")
                                dpg.add_text(UserNameL,tag="LoginInfo5")
                        with dpg.menu(label="Music Player"):
                                dpg.add_menu_item(label="Go to music player",callback=_MusicPlayerWindow)
                                dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying9")
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying10")
                dpg.add_text("The config menu")
                with dpg.group(horizontal=False):
                        with dpg.child_window(width=500, height=270,autosize_x=True):
                                with dpg.group(horizontal=False):
                                        with dpg.group(horizontal=True):
                                                dpg.add_checkbox(label="Fullscreen?",tag="FullScreenCheck", callback=_Config)
                                                items = ("600x700","900x900","1280x720")
                                                ResolutionCombo = dpg.add_combo(items, label="Screen Resolution",tag="ScreenResolutionCombo",height_mode=dpg.mvComboHeight_Small,callback=_Config,default_value="600x700")
                                        dpg.add_checkbox(label="Maximize?",tag="MaximizeCheck", callback=_Config)
                                        with dpg.group(horizontal=False):
                                                with dpg.group(horizontal=True):
                                                        dpg.add_text("Current Resolution: ")
                                                        dpg.add_text(label=str(ViewPortWidth)+"x"+str(ViewPortHeight),tag="CResolution")
                                                dpg.configure_item(item="CResolution",tag="CResolution",color=(0,255,0))
                                with dpg.group(horizontal=True):
                                        dpg.add_text(tag="CSVfeature",label="")
                                dpg.add_input_text(label='Download Path: Default path is ./DL/',tag="DLPath", width=300, hint='E:\Downloads',callback=_CurrentPath)
                                dpg.add_button(label="Directory Explorer",callback=_FileExplorer)
                                dpg.add_text(label="",tag="CurrentPath")
                                dpg.add_text(label="",tag="IsPathValid")
                                Themes = ("Red & White","Ice Cold","Love-Colored Stars","Heaven")
                                ThemeCombo = dpg.add_combo(Themes, label="Theme selector",tag="ThemeSelectorTag",height_mode=dpg.mvComboHeight_Small,callback=_ThemeSelector)

        with dpg.window(tag="Login_Menu",show=False):
                with dpg.menu_bar():
                        with dpg.menu(label="Home"):
                                dpg.add_menu_item(label="Go Home",callback=_GoHome)
                                with dpg.menu(label="About"):
                                        dpg.add_text("The THMD or TouHou Music Database is a small but appasionate proyect\nthat started as a small script where you could input the information\nof your favorite remixes/songs/musics that are about Touhou.\n\nThe more i developed this proyect the more i felt i had to improve\nso it was some sort of feedback loop of error and succes eventually\nhitting a point of needing a GUI.\nthe GUI library in question is DearPyGUI and it's very genuine and easy to use.\n\nI love DearPyGUI for it's simplicity yet it's versatility.\nThis was written in V0.01")
                                        with dpg.tooltip(dpg.last_item()):
                                                dpg.add_text("(東方) Music Database")
                        with dpg.menu(label="Login"):
                                dpg.add_button(label="Login menu",callback=_LoginMenu)
                                dpg.add_text("Logged as: ")
                                dpg.add_text(UserNameL,tag="LoginInfo6")
                        with dpg.menu(label="Music Player"):
                                dpg.add_menu_item(label="Go to music player",callback=_MusicPlayerWindow)
                                dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying11")
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying12")
                dpg.add_text("The Login Menu")
                with dpg.child_window(width=500, height=200,autosize_x=True):
                        with dpg.group(horizontal=False,tag="LoginForm"):
                                UserNameL = dpg.add_input_text(label="UserName",width=450, callback=_Username)
                                PassWordL = dpg.add_input_text(label="Password",width=450,password=True, callback=_Password)
                                dpg.add_button(label="Login",callback=_LoginConnection)
                                dpg.add_text(label="",tag="LoginTextInfo")

        with dpg.window(tag="Music_Player_Window",show=False):
                with dpg.menu_bar():
                        with dpg.menu(label="Home"):
                                dpg.add_menu_item(label="Go Home",callback=_GoHome)
                                with dpg.menu(label="About"):
                                        dpg.add_text("The THMD or TouHou Music Database is a small but appasionate proyect\nthat started as a small script where you could input the information\nof your favorite remixes/songs/musics that are about Touhou.\n\nThe more i developed this proyect the more i felt i had to improve\nso it was some sort of feedback loop of error and succes eventually\nhitting a point of needing a GUI.\nthe GUI library in question is DearPyGUI and it's very genuine and easy to use.\n\nI love DearPyGUI for it's simplicity yet it's versatility.\nThis was written in V0.01")
                                        with dpg.tooltip(dpg.last_item()):
                                                dpg.add_text("(東方) Music Database")
                        with dpg.menu(label="Login"):
                                dpg.add_button(label="Login menu",callback=_LoginMenu)
                                dpg.add_text("Logged as: ")
                                dpg.add_text(UserNameL,tag="LoginInfo7")
                        with dpg.menu(label="Music Player"):
                                dpg.add_menu_item(label="Go to music player",callback=_MusicPlayerWindow)
                                dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying13")
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying14")
                with dpg.group(horizontal=True):
                        dpg.add_text("The Music Player Window")
                        MusicPlayerInfo = ("Local data","DB data")
                        MusicDataCombo = dpg.add_combo(items=MusicPlayerInfo, label="Music data selector",tag="MusicDataSelector",height_mode=dpg.mvComboHeight_Small,callback=_MusicDataCombo)
                dpg.add_button(label="Playlist",height=20,tag="PlaylistTag",show=False,callback=_ShowPlaylistMenu)
                dpg.hide_item(item="MusicDataSelector")
                with dpg.group(horizontal=False,tag="LJsonFiles"):
                        dpg.add_button(label="Load local Json",width=-1,height=50,tag="ReJsonLoad", callback=_LoadJson)
                        dpg.add_button(label="Load DB Json",width=-1, height=50, tag="MusicPLoadDBJson",callback=_LoadDBJson)
                with dpg.child_window(height=23,border=False,autosize_x=True):
                        with dpg.group(horizontal=False,tag="MusicPlayer"):
                                dpg.add_text("",tag="IsDataLoaded")

        with dpg.window(label="Playlist menu",tag="MusicPlaylists",show=False, width=460,height=150,pos=[120,150]):
                with dpg.group(horizontal=True):
                        dpg.add_text("Listening to: ",tag="WhatMusicIsPlaying15")
                with dpg.tab_bar():
                        with dpg.tab(label="Add"):
                                dpg.add_button(label="Create a new playlist!",parent="MusicPlaylist",callback=_CreatePlaylist)
                        with dpg.tab(label="Select",tag="SelectTag"):
                                PlaylistItems = os.listdir('./Json/Playlist/')
                                for item in PlaylistItems:
                                        print(item)
                                        ItemsList.append(item)
                                print(ItemsList)
                                dpg.add_combo(items=ItemsList, label="Select a playlist",tag="PlaylistSelector",callback=_PlaylistSelector)

_SavedTheme()
dpg.bind_item_handler_registry("FullScreenCheck", "widget handler")

dpg.set_viewport_small_icon("./src/TohoMusicDatabase.ico")
dpg.set_viewport_large_icon("./src/TohoMusicDatabase.ico")

dpg.show_viewport()
dpg.set_primary_window("MainMenu", True)
dpg.start_dearpygui()
dpg.destroy_context()

