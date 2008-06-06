from datetime import datetime
from mod_python.Session import Session 
from Cheetah.Template import Template

def checkAllowed(reservation, oid):
	return reservation.getReservatorOid() == oid

def extractTuple(strng):
	l = strng.strip().split(':', 2)
	if len(l) < 2:
		return (None,None)
	
	ia = int(l[0])
	ib = int(l[1])
	if not ( 0 <= ia <= 23 and 0 <= ib <= 59 ):
		return (None,None)

	return (ia,ib)

class EditModule:

	_dir = '/home/moorwww/public_html/pizza'

	def __init__(self, req, page, oid, dic):
		self._page = page
		self._oid = int(oid)
		self._dic = dic
		page.setTitle('Editieren')

	def write(self):
		t = Template(file=self._dir+'/templates/edit.tmpl')

		reservation = self._page._db.loadReservationOID(int(self._oid))
		if reservation and checkAllowed(reservation, self._page._login.getOid()):
			t.reservation = reservation
			t.message = None
			t.goodmessage = None
			if self._dic and self._dic.has_key('submit'):
				(sh,sm) = extractTuple(self._dic['start'])
				(eh,em) = extractTuple(self._dic['end'])
				desc = unicode(self._dic['description'], 'latin-1')

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

	_dir = '/home/moorwww/public_html/pizza'

	def __init__(self, req, page, oid, confirm):
		self._page = page
		self._oid = int(oid)
		self._confirm = int(confirm)
		page.setTitle('L&ouml;schen')
	
	def write(self):
		t = Template(file=self._dir+'/templates/delete.tmpl')

		r = self._page._db.loadReservationOID(self._oid)
		if r and checkAllowed(r, self._page._login.getOid()) and r._to > datetime.now():
		
			t.r = r		
			t.deleted = False
			if self._oid == self._confirm:
				t.deleted = True
				r.delete()
		
		else:
			t.r = None

		return t

class NewModule:

	_dir = '/home/moorwww/public_html/pizza'

	def __init__(self, req, page, dic):
		self._page = page
		self._dic = dic
		page.setTitle('Neue Reservation')
	
	def write(self):
		t = Template(file=self._dir+'/templates/new.tmpl')

		t.message = []
		t.goodmessage = ''
		t.showform = True
		

		if self._dic and self._dic.has_key('submit'):
			t.data = { 'day':self._dic['day'], 'month':self._dic['month'], 'year':self._dic['year'], 'start':self._dic['start'], 'end':self._dic['end'], 'description':self._dic['description'] }

			self._dic['day'] = int(self._dic['day'])
			self._dic['month'] = int(self._dic['month'])
			self._dic['year'] = int(self._dic['year'])

			(sh,sm) = extractTuple(self._dic['start'])
                        (eh,em) = extractTuple(self._dic['end'])

			desc = unicode(self._dic['description'],'latin-1')

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

			if not ( 1 <= self._dic['day'] <= 31 ):
				t.message.append('Ung&uuml;ltiger Tag')
				ok = False
				
			if not ( 1 <= self._dic['month'] <= 12 ):
				t.message.append('Ung&uuml;ltiger Monat')
				ok = False
			
			if not ( 2005 <= self._dic['year'] <= 2010 ):
				t.message.append('Ung&uuml;ltiges Jahr')
				ok = False

			if ok:
				when = datetime(self._dic['year'], self._dic['month'], self._dic['day'], eh, em, 0)
				if when < datetime.now():
					t.message.append('Termin liegt in der Vergangenheit')
					ok = False

			if ok:
				start = datetime(self._dic['year'], self._dic['month'], self._dic['day'], sh, sm, 0)
				end = datetime(self._dic['year'], self._dic['month'], self._dic['day'], eh, em, 0)
				self._page._db.newReservation(self._page._login.getOid(),
					start,
					end,
					desc)
				t.goodmessage = "Der Termin wurde reserviert"
				t.showform = False

		else:
			t.data = { 'day':datetime.now().day, 'month':datetime.now().month, 'year':datetime.now().year, 'start':'16:00', 'end':'22:00', 'description':'' }

		return t

