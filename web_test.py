#coding:UTF-8
import web
import os
import re
import random
from plot_zhihu import PlotZhihu
   
class SearchForm:
    
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, "templates")
        self.render = web.template.render(self.templates_root)
        
        plot_object = PlotZhihu()
        self.names_all = plot_object.get_names()
        
    def GET(self):
        
        data = web.input()
        try:
            self.name = data.search_form
        except:
            return self.render.index(None, 0)
            
        #check if the navication url
        if self.name in {"private", "contact", "other", "description"}:
            return self.render.index(self.name, 3)
            
        if self.name in self.names_all:
            return self.render.index(self.name, 1)
        else:
            self.name = self.search_name()
            return self.render.index(self.name, 2)
                
        
    def search_name(self):
        '''
        fuzzy match the name
        '''
        names_temp = set([])
        
        #remove the space
        name_split = self.name.split(" ")
        self.name = ""
        for item in name_split:
            self.name += item
            
        sentence = "("
        for idx in range(len(self.name)):
            sentence += '.*' + self.name[idx]
        pattern = re.compile(sentence + '.*)')
        for name in self.names_all:
            names_temp.update(set(pattern.findall(name)))
        if names_temp:
            #forward match and backward match
            try:
                #if too many, choice three items among all
                names_answer = random.sample(names_temp, 3)
            except(ValueError):
                names_answer = names_temp
            return names_answer
        else:
            #keyword search
            for idx in range(len(self.name)):
                sentence += '.*' + self.name[idx] + '|'
            pattern = re.compile(sentence[:-1] + ')')
            for name in self.names_all:
                names_temp.update(set(pattern.findall(name)))
            if names_temp:
                #forward match and backward match
                try:
                    #if too many, choice three items among all
                    names_answer = random.sample(names_temp, 3)
                except(ValueError):
                    names_answer = names_temp
                return names_answer
        
        #if found nothing, random choice from the all names.
        return random.sample(self.names_all, 3)
            
        
class GeImage:
    
    def __init__(self):
        pass
        
    def GET(self):
        data = web.input(name=None)
        self.name = data.name
        
        if not self.name:
            return u"哦，程序崩溃了。可以的话请发邮件给我：gting405@gmail.com。不过我的周末..."
            
        plot_object = PlotZhihu()
        plot_object.search_time(self.name)
        self.buf = plot_object.plot()
        self.buf.seek(0)
        self.contents = self.buf.getvalue()
        return self.contents
        

    