from google.appengine.ext import ndb

class Igra(ndb.Model):

    ugani = ndb.StringProperty()

class Kontakt(ndb.Model):
    ime_in_priimek = ndb.StringProperty()
    opis = ndb.StringProperty()
    email = ndb.StringProperty()

class Komentar(ndb.Model):
    uporabnisko_ime = ndb.StringProperty()
    mail = ndb.StringProperty()
    komentar = ndb.TextProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)