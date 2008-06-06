from mod_python import apache
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

MainPage = apache.import_module('MainPage')
ListingModule = apache.import_module('ListingModule')
EditModule = apache.import_module('EditModule')

def index(req):
	pg = MainPage.MainPage(req)
	return pg.write()

def logout(req):
	pg = MainPage.MainPage(req)
	pg._login.logout()
	return pg.write()

def login(req, user='', password=''):
	pg = MainPage.MainPage(req)
	pg._main = ListingModule.ListingModule(req, pg)
	pg._login.login(user, password)
	return pg.write()

def listing(req):
	pg = MainPage.MainPage(req)
	pg._main = ListingModule.ListingModule(req, pg)
	return pg.write()

def edit(req, oid=0, **dic):
	pg = MainPage.MainPage(req)
	pg._main = EditModule.EditModule(req, pg, oid, dic)
	return pg.write()

def delete(req, oid=0, confirm=-1):
	pg = MainPage.MainPage(req)
	pg._main = EditModule.DeleteModule(req, pg, oid, confirm)
	return pg.write()

def new(req, **dic):
	pg = MainPage.MainPage(req)
	pg._main = EditModule.NewModule(req, pg, dic)
	return pg.write()

