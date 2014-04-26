from src import LoginModule, WelcomeModule, PizzaDB
from Cheetah.Template import Template

class MainPage:

  def __init__(self, req, main=None):
    self._db = PizzaDB.PizzaDB()
    self._login = LoginModule.LoginModule(req, self)
    self._main = main
    self._title = 'Pizzaofen'

  def write(self, response):
    t = Template(file='templates/page.tmpl')
    if self._main and self._login.isLoggedIn():
      t.body = self._main.write()
    else:
      t.body = WelcomeModule.WelcomeModule(self).write()

    t.login = self._login.write()
    t.title = self._title
    response.write(str(t))

  def setTitle(self, title):
    self._title = 'Pizzaofen: '+title
