from Crypto.Hash import SHA256

class User:
  
  def __init__(self, oid, username, password, real, db):
    self._oid = int(oid)
    self._username = username
    self._password = password
    self._realname = real
    self._db = db
    
  def checkPassword(self, password):
    to_hash = "%d:%s" % (self._oid, password)
    hash = SHA256.new(to_hash).hexdigest()
    return hash == self._password
      
  def __str__(self):
    return self._username + ' (' + self._realname + ')'
  
  def getName(self):
    return self._realname

  def getOid(self):
    return self._oid
      
      
class Reservation:

  def __init__(self, oid, user_oid, frm, to, description, db):
    self._oid = int(oid)
    self._reservator = int(user_oid)
    self._from = frm
    self._to = to
    self._description = description
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
