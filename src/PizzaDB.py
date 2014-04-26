from google.appengine.ext import db

from src import Types

class User(db.Model):
  real_name = db.StringProperty()
  user_name = db.StringProperty()
  password = db.StringProperty()

class Reservation(db.Model):
  starting = db.DateTimeProperty()
  ending = db.DateTimeProperty()
  description = db.TextProperty()

class PizzaDB:
  def __init__(self):
    self._user_cache = {}

  def loadUserID(self, id):
    if id in self._user_cache:
      return self._user_cache[id]

    user = db.get(db.Key.from_path("User", id))
    if user:
      user = Types.User(user.key().id(), user.user_name, user.password, user.real_name, self)
      self._user_cache[id] = user
      return user

  def loadUserName(self, username):
    q = User.all()
    q.filter("user_name =", username)
    users = list(q.run(limit = 2))
    if len(users) != 1:
      return None
    user = users[0]
    return Types.User(user.key().id(), user.user_name, user.password, user.real_name, self)
        
  def getReservations(self, start):
    q = Reservation.all()
    q.filter("starting >", start)
    l = []
    for r in q.run(limit = 50):
      l.append(Types.Reservation(r.key().id(), r.key().parent().id(), r.starting, r.ending, r.description, self))
    return l
  
  def loadReservationOID(self, user_id, reservation_id):
    k = db.Key.from_path("Reservation", reservation_id, parent=db.Key.from_path("User", user_id))
    r = db.get(k)
    if r:
      return Types.Reservation(r.key().id(), r.key().parent().id(), r.starting, r.ending, r.description, self)

  def newReservation(self, owner, start, end, description):
    r = Reservation(parent=db.Key.from_path("User", owner))
    r.starting = start
    r.ending = end
    r.description = description
    r.put()

  def updateReservation(self, reservation):
    k = db.Key.from_path("Reservation", reservation._oid, parent=db.Key.from_path("User", reservation._reservator))
    r = db.get(k)
    r.starting = reservation._from
    r.ending = reservation._to
    r.description = reservation._description
    r.put()

  def deleteReservation(self, reservation):
    k = db.Key.from_path("Reservation", reservation._oid, parent=db.Key.from_path("User", reservation._reservator))
    db.delete(k)
