from mod_python.Session import Session 
from Cheetah.Template import Template

class WelcomeModule:

    _dir = '/home/httpd/htdocs/pizza'

    def __init__(self, page):
        page.setTitle('Willkommen')
    
    def write(self):
	t = Template(file=self._dir+'/templates/welcome.tmpl')
	return t
