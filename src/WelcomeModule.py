from Cheetah.Template import Template

class WelcomeModule(object):

  def __init__(self, page):
    page.setTitle('Willkommen')

  def write(self):
    return Template(file='templates/welcome.tmpl')
