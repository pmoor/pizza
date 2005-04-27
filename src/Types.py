import sha
from datetime import datetime

class User:
	
	_oid = None
	_username = None
	_password = None
	_realname = None
	
        _db = None

	def __init__(self, dict, db):
		self._oid = dict['uid']
		self._username = dict['username']
		self._password = dict['password']
		self._realname = dict['realName']
		
                self._db = db
		
        def checkPassword(self, password):
	    #s = sha.sha()
	    #s.update(password)
	    #return self._password == s.hexdigest()
	    return self._password == password
	    
        def __str__(self):
	    return self._username + ' (' + self._realname + ')'
	
	def getName(self):
		return self._realname

	def getOid(self):
		return self._oid
	    
	    
class Reservation:

	_oid = None
	_reservator = None
	_from = None
	_to = None
	_description = None
	
        _db = None

	def __init__(self, dict, db):
		self._oid = int(dict['uid'])
		self._reservator = int(dict['user_uid'])
		self._from = datetime.fromtimestamp(dict['starting'])
		self._to = datetime.fromtimestamp(dict['ending'])
                self._description = unicode(dict['description'], 'utf8')
                self._db = db
       
	def update(self):
		self._db.updateReservation(self)
       
        def delete(self):
		self._db.deleteReservation(self)
		
	def __str__(self):
	    return self._description + ' (' + str(self._from) + ' - ' + str(self._to) + ')'

	def __repr__(self):
	    return self.__str__()
	    
        def getReservator(self):
	    return self._db.loadUserID(self._reservator)

	def getDay(self):
	    return self._from.strftime('%A, %d. %B %Y')
	
	def getStart(self):
	    return self._from.strftime('%H:%M')
	
	def getEnd(self):
	    return self._to.strftime('%H:%M')

	def getWho(self):
	    return self.getReservator().getName()
	
	def getReservatorOid(self):
	    return self.getReservator().getOid()

	def getOid(self):
	    return self._oid

	def getDescription(self):
		return self._description
