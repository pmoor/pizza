from mod_python import apache
LoginModule = apache.import_module('LoginModule')
WelcomeModule = apache.import_module('WelcomeModule')
PizzaDB = apache.import_module('PizzaDB')
from Cheetah.Template import Template
import locale

class MainPage:
	_title = ''
	_dir = '/home/moorwww/public_html/pizza'
	_login = None
	_main = None

	def __init__(self, req, main=None):
		self._db = PizzaDB.PizzaDB()
		self._login = LoginModule.LoginModule(req, self)
		self._main = main
		self._title = 'Pizzaofen'

	def write(self):
		t = Template(file=self._dir+'/templates/page.tmpl')
		if self._main and self._login.isLoggedIn():
			t.body = self._main.write()
		else:
			t.body = WelcomeModule.WelcomeModule(self).write()
		
		t.login = self._login.write()
		t.title = self._title
		s = str(t)
		self._db.clean()
		return s

	def setTitle(self, title):
		self._title = 'Pizzaofen: '+title

