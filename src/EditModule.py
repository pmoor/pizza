from datetime import datetime
from Cheetah.Template import Template


def extractTuple(strng):
  l = strng.strip().split(':', 2)
  if len(l) < 2:
    return (None, None)

  ia = int(l[0])
  ib = int(l[1])
  if not ( 0 <= ia <= 23 and 0 <= ib <= 59 ):
    return (None, None)

  return (ia, ib)

class EditModule:

  def __init__(self, req, page):
    self._page = page
    self._dic = req.request.params
    self._oid = int(req.request.params["oid"])
    page.setTitle('Editieren')

  def write(self):
    t = Template(file='templates/edit.tmpl')

    reservation = self._page._db.loadReservationOID(self._page._login.getOid(), self._oid)
    if reservation:
      t.reservation = reservation
      t.message = None
      t.goodmessage = None
      if self._dic and self._dic.has_key('submit'):
        (sh,sm) = extractTuple(self._dic['start'])
        (eh,em) = extractTuple(self._dic['end'])
        desc = self._dic['description']

        t.message = ''
        ok = True
        if sh == None:
          t.message += "Ung&uuml;ltige Startzeit"
          ok = False

        if eh == None:
          t.message += "Ung&uuml;ltige Endzeit"
          ok = False

        if ok:
          if sh > eh  or  sh == eh and sm >= em:
            t.message += "Startzeit liegt nach Endzeit"
            ok = False

        if ok:
          olds = reservation._from
          newstart = datetime(olds.year, olds.month, olds.day, sh, sm, 0)
          olde = reservation._to
          newend = datetime(olde.year, olde.month, olde.day, eh, em, 0)

          reservation._from = newstart
          reservation._to = newend
          reservation._description = desc

          reservation.update()

          t.goodmessage = "Ok, &Auml;nderungen vorgenommen"
    else:
      t.reservation = None

    return t

class DeleteModule:

  def __init__(self, req, page,):
    self._page = page
    self._dic = req.request.params
    self._oid = int(req.request.params["oid"])
    self._confirm = None
    if "confirm" in req.request.params:
      self._confirm = int(req.request.params["confirm"])
    page.setTitle('L&ouml;schen')

  def write(self):
    t = Template(file='templates/delete.tmpl')

    r = self._page._db.loadReservationOID(self._page._login.getOid(), self._oid)
    if r and r._to > datetime.now():
      t.r = r
      t.deleted = False
      if self._oid == self._confirm:
        t.deleted = True
        r.delete()
    else:
      t.r = None

    return t

class NewModule:

  def __init__(self, req, page,):
    self._page = page
    self._dic = req.request.params
    page.setTitle('Neue Reservation')

  def write(self):
    t = Template(file='templates/new.tmpl')

    t.message = []
    t.goodmessage = ''
    t.showform = True

    if self._dic and self._dic.has_key('submit'):
      t.data = { 'day':self._dic['day'], 'month':self._dic['month'], 'year':self._dic['year'], 'start':self._dic['start'], 'end':self._dic['end'], 'description':self._dic['description'] }

      day = int(self._dic['day'])
      month = int(self._dic['month'])
      year = int(self._dic['year'])

      (sh, sm) = extractTuple(self._dic['start'])
      (eh, em) = extractTuple(self._dic['end'])

      desc = self._dic['description']

      ok = True
      if sh == None:
        t.message.append('Ung&uuml;ltige Startzeit')
        ok = False

      if eh == None:
        t.message.append('Ung&uuml;ltige Endzeit')
        ok = False

      if ok:
        if sh > eh  or  sh == eh and sm >= em:
          t.message.append('Startzeit liegt nach Endzeit')
          ok = False

      if not (1 <= day <= 31 ):
        t.message.append('Ung&uuml;ltiger Tag')
        ok = False

      if not ( 1 <= month <= 12 ):
        t.message.append('Ung&uuml;ltiger Monat')
        ok = False

      if not ( 2005 <= year <= 2100 ):
        t.message.append('Ung&uuml;ltiges Jahr')
        ok = False

      if ok:
        when = datetime(year, month, day, eh, em, 0)
        if when < datetime.now():
          t.message.append('Termin liegt in der Vergangenheit')
          ok = False

      if ok:
        start = datetime(year, month, day, sh, sm, 0)
        end = datetime(year, month, day, eh, em, 0)
        self._page._db.newReservation(self._page._login.getOid(),
          start,
          end,
          desc)
        t.goodmessage = "Der Termin wurde reserviert"
        t.showform = False

    else:
      t.data = { 'day':datetime.now().day, 'month':datetime.now().month, 'year':datetime.now().year, 'start':'16:00', 'end':'22:00', 'description':'' }

    return t

