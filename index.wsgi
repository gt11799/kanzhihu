#coding:UTF-8
import sae

import os
import web

from web_test import SearchForm, GeImage


urls = (
    "/", "SearchForm",
	"/hello", "Hello",
	"/image", "GeImage",
	"/(.*)","Hello",
	)
	
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Hello:
    def GET(self):
        return "hello"
		
app = web.application(urls, globals()).wsgifunc()		
application = sae.create_wsgi_app(app)
