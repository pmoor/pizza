import webapp2
from src import MainPage, ListingModule, EditModule

class RootHandler(webapp2.RequestHandler):
  def get(self):
    pg = MainPage.MainPage(self)
    pg.write(self.response)

class LogoutHandler(webapp2.RequestHandler):
  def get(self):
    pg = MainPage.MainPage(self)
    pg._login.logout()
    pg.write(self.response)

class LoginHandler(webapp2.RequestHandler):
  def post(self):
    self.get()

  def get(self):
    pg = MainPage.MainPage(self)
    pg._main = ListingModule.ListingModule(self, pg)
    pg._login.login(self.request.get('user'), self.request.get('password'))
    pg.write(self.response)

class ListingHandler(webapp2.RequestHandler):
  def get(self):
    pg = MainPage.MainPage(self)
    pg._main = ListingModule.ListingModule(self, pg)
    pg.write(self.response)

class NewHandler(webapp2.RequestHandler):
  def post(self):
    self.get()

  def get(self):
    pg = MainPage.MainPage(self)
    pg._main = EditModule.NewModule(self, pg)
    pg.write(self.response)

class EditHandler(webapp2.RequestHandler):
  def post(self):
    self.get()

  def get(self):
    pg = MainPage.MainPage(self)
    pg._main = EditModule.EditModule(self, pg)
    pg.write(self.response)

class DeleteHandler(webapp2.RequestHandler):
  def post(self):
    self.get()

  def get(self):
    pg = MainPage.MainPage(self)
    pg._main = EditModule.DeleteModule(self, pg)
    pg.write(self.response)

app = webapp2.WSGIApplication(
    [(r'/', RootHandler),
     (r'/logout', LogoutHandler),
     (r'/login', LoginHandler),
     (r'/new', NewHandler),
     (r'/edit', EditHandler),
     (r'/delete', DeleteHandler),
     (r'/listing', ListingHandler)])
