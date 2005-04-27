from mod_python.Session import Session 
from Cheetah.Template import Template

class LoginModule:

	_dir = '/home/httpd/htdocs/pizza'
	_sess = None    
	_reason = ''

	def __init__(self, req, page):
		self._sess = Session(req)
		self._page = page
		self._reason = ''
		self._user = None
		if self.isLoggedIn():
			self._user = page._db.loadUserName(self.getUser())


	def isLoggedIn(self):
		return self._sess and self._sess['login']

	def write(self):
		t = Template(file=self._dir+'/templates/login.tmpl')
		t.loggedin = self.isLoggedIn()
		if t.loggedin:
			t.user = self._sess['login']

		else:
			t.reason = self._reason

		return t

	def logout(self):
		self._sess['login'] = ''
		self._sess.save()
		self._user = None

	def login(self, user, password):
		u = self._page._db.loadUserName(user)
		if not u:
			self._reason = 'Unbekannter Benutzer oder falsches Passwort'
			return False

		if not u.checkPassword(password):
			self._reason = 'Unbekannter Benutzer oder falsches Passwort'
			return False

		self._sess['login'] = user
		self._sess.save()
		self._user = u
		return True

	def getUser(self):
		return self._sess['login']

	def getOid(self):
		if not self._user:
			return -1

		return self._user.getOid()

