import _pg
from mod_python import apache
Types = apache.import_module('Types')
from re import escape

def format_datetime(dtime):
	return '%d-%d-%d %d:%d:%d' % (dtime.year, dtime.month, dtime.day, dtime.hour, dtime.minute, dtime.second)

class PizzaDB:

	_user = 'pizza'
	_database = 'pizza'
	_password = 'srN5C1ij'
	_host = 'spyro.moor.ws'

	_db = None

	def __init__(self):
		try:
			self._db = _pg.connect( dbname = self._database,
						host = self._host,
						user = self._user,
						passwd = self._password )
			self._db.query('SET client_encoding TO UNICODE')
		except:
			self._db = None

	def clean(self):
		if self._db != None:
			self._db.close()
			self._db = None

	def loadUserID(self, id):
		res = self._db.query('SELECT * FROM users WHERE uid = %d' % id)
		dic = res.dictresult()[0]
		usr = Types.User(dic, self)
		return usr

	def loadUserName(self, username):
		res = self._db.query('SELECT * FROM users WHERE username = \'%s\'' % escape(username))
		if not res.dictresult():
			return None

		dic = res.dictresult()[0]
		usr = Types.User(dic, self)
		return usr
        
        def getReservations(self, start, end, user=None):
	    wherepart = 'WHERE ending > \'%s\' AND starting < \'%s\'' % (start, end);
	    if user:
		wherepart += ' AND user_uid = ' + user._uid
		
	    query = 'SELECT uid,\
	    EXTRACT(EPOCH FROM starting) AS starting,\
	    EXTRACT(EPOCH FROM ending) AS ending,\
	    description,user_uid FROM reservations %s ORDER BY starting' % wherepart;
	    res = self._db.query(query)
	    ret = []
	    for dic in res.dictresult():
		ret.append(Types.Reservation(dic, self))
	    return ret
	
	def loadReservationOID(self, oid):
		query = 'SELECT uid,\
		EXTRACT(EPOCH FROM starting) AS starting,\
		EXTRACT(EPOCH FROM ending) AS ending,\
		description,user_uid FROM reservations WHERE uid = %d' % int(oid);
		res = self._db.query(query)
		if not res.dictresult():
			return None

		return Types.Reservation(res.dictresult()[0], self)

        def newReservation(self, owner, start, end, description):
	    desc = escape(description.encode('utf8'))
	    query = 'INSERT INTO reservations (starting,ending,description,user_uid) VALUES (\'%s\',\'%s\',\'%s\',%d)' % (format_datetime(start), format_datetime(end), desc, int(owner));
	    res = self._db.query(query)

	def updateReservation(self, r):
		desc = escape(r._description.encode('utf8'))
		query = 'UPDATE reservations SET starting = \'%s\', ending = \'%s\', description = \'%s\' WHERE uid = %d' % (format_datetime(r._from), format_datetime(r._to), desc, int(r._oid));
		res = self._db.query(query)

	def deleteReservation(self, r):
		query = 'DELETE FROM reservations WHERE uid = %d' % r.getOid();
		res = self._db.query(query)

