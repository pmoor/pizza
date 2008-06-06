from mod_python import apache
Types = apache.import_module('Types')
MySQLdb = apache.import_module('MySQLdb')
from re import escape

def format_datetime(dtime):
	return '%d-%d-%d %d:%d:%d' % (dtime.year, dtime.month, dtime.day, dtime.hour, dtime.minute, dtime.second)

class PizzaDB:

	def __init__(self):
		self._user = 'moor-pizza'
		self._database = 'moor-pizza'
		self._password = 'srN5C1ij'
		self._host = 'localhost'
		self._socket = '/var/lib/mysql/mysql.sock'

		self._db = MySQLdb.connect(db = self._database,
					   host = self._host,
					   user = self._user,
					   passwd = self._password,
                                           unix_socket = self._socket)
		self._db.query('SET CHARACTER SET utf8')

	def clean(self):
		if self._db != None:
			self._db.close()
			self._db = None

	def loadUserID(self, id):
	        query = 'SELECT oid, user, password, realName FROM users WHERE oid = %d' % id
		cursor = self._db.cursor()
		cursor.execute(query)
		row = cursor.fetchone()
		return Types.User(row[0], row[1], row[2], row[3], self)

	def loadUserName(self, username):
	        query = 'SELECT oid, user, password, realName FROM users WHERE user = \'%s\'' % escape(username)
		cursor = self._db.cursor()
		cursor.execute(query)
		if cursor.rowcount != 1:
			return None
		row = cursor.fetchone()
		return Types.User(row[0], row[1], row[2], row[3], self)
        
        def getReservations(self, start, end):
	    wherepart = 'WHERE `ending` > \'%s\' AND `starting` < \'%s\'' % (start, end);
	    query = 'SELECT oid,\
	    UNIX_TIMESTAMP(`starting`) AS start,\
	    UNIX_TIMESTAMP(`ending`) AS end,\
	    description,\
	    user_oid\
	    FROM reservations %s ORDER BY `starting`' % wherepart;
	    cursor = self._db.cursor()
	    cursor.execute(query)
	    result = cursor.fetchall()
	    ret = []
	    for row in result:
		ret.append(Types.Reservation(row[0], row[4], row[1], row[2], row[3], self))
	    return ret
	
	def loadReservationOID(self, oid):
		query = 'SELECT oid,\
		UNIX_TIMESTAMP(`starting`) AS start,\
		UNIX_TIMESTAMP(`ending`) AS end,\
		description,\
		user_oid\
		FROM reservations WHERE oid = %d' % int(oid);
		cursor = self._db.cursor()
		cursor.execute(query)
		if cursor.rowcount != 1:
			return None
		row = cursor.fetchone()
		return Types.Reservation(row[0], row[4], row[1], row[2], row[3], self)

        def newReservation(self, owner, start, end, description):
	    desc = escape(description.encode('utf8'))
	    query = 'INSERT INTO reservations (`starting`,`ending`,`description`,`user_oid`) VALUES (\'%s\',\'%s\',\'%s\',%d)' % (format_datetime(start), format_datetime(end), desc, int(owner));
	    res = self._db.query(query)

	def updateReservation(self, r):
		desc = escape(r._description.encode('utf8'))
		query = 'UPDATE reservations SET `starting` = \'%s\', `ending` = \'%s\', `description` = \'%s\' WHERE `oid` = %d' % (format_datetime(r._from), format_datetime(r._to), desc, int(r._oid));
		res = self._db.query(query)

	def deleteReservation(self, r):
		query = 'DELETE FROM reservations WHERE oid = %d' % r.getOid();
		res = self._db.query(query)

