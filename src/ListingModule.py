from datetime import date, timedelta
from Cheetah.Template import Template


class ListingModule(object):

  def __init__(self, req, page):
    self._page = page
    page.setTitle('&Uuml;bersicht')

  def write(self):
    t = Template(file='templates/listing.tmpl')
    t.reservations = self._page._db.getReservations(date.today()-timedelta(days=2))
    t.oid = self._page._login.getOid()
    return t
