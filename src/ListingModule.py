from datetime import date, timedelta
from mod_python.Session import Session 
from Cheetah.Template import Template


class ListingModule:

    _dir = '/home/httpd/htdocs/pizza'

    def __init__(self,req,page):
        self._page = page
	page.setTitle('&Uuml;bersicht')
    
    def write(self):
	t = Template(file=self._dir+'/templates/listing.tmpl')

	t.reservations = self._page._db.getReservations(date.today()-timedelta(days=2),date(2015,1,1))
	t.oid = self._page._login.getOid()
	
	return t
