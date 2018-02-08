#!/usr/bin/env python
import os
import jinja2
import webapp2
import json
import random
import hmac

from models import Igra
from models import Kontakt
from models import Komentar
from google.appengine.api import users


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class HomeHandler(BaseHandler):
    def get(self):
        return self.render_template('base.html')

class NoviceHandler(BaseHandler):
    def get(self):
        komentar_clanka = Komentar.query().fetch()
        params = {"komentar_clanka": komentar_clanka}


        return self.render_template('novice.html', params=params)

    def post(self):
        komentar = self.request.get("komentar")
        mail = self.request.get("mail")
        uporabnisko_ime = self.request.get("uporabnisko_ime")


        komentar_clanka=Komentar(komentar=komentar, mail=mail, uporabnisko_ime=uporabnisko_ime)

        komentar_clanka.put()

        self.write(komentar_clanka)

        return self.render_template("novice.html")



class IgraHandler(BaseHandler):
    def get(self):

        with open("mesta.json","r") as j_file:
            json_raw = j_file.read()
            json_data = json.loads(json_raw)

            odgovor = self.request.get("odgovor")
            drzava = self.request.get("drzava")

            for drzave in j_file:
                if odgovor("mesto")==drzava:
                    return "bravo!"
                else:
                    return "poskusi se enkrat!"
        return self.render_template('igra.html')

    def post(self):

        drzava = self.request.get("ugani")





class KontaktHandler(BaseHandler):
    def get(self):
        return self.render_template('kontakt.html')

    def post(self):

        ime_in_priimek = self.request.get("ime_in_priimek")
        email = self.request.get("email")
        opis = self.request.get("opis")


        kontakt = Kontakt(ime_in_priimek=ime_in_priimek, email=email, opis=opis)

        kontakt.put()

        return self.render_template('odgovor.html')

class OdgovorHandler(BaseHandler):
    def get(self):
        return self.render_template('odgovor.html')


class OmeniHandler(BaseHandler):
    def get(self):
        return self.render_template('o_meni.html')


app = webapp2.WSGIApplication([

    webapp2.Route('/', HomeHandler),
    webapp2.Route('/novice', NoviceHandler, name="novice"),
    webapp2.Route('/igra', IgraHandler),
    webapp2.Route('/kontakt', KontaktHandler),
    webapp2.Route('/odgovor', OdgovorHandler),
    webapp2.Route('/o meni', OmeniHandler),

], debug=True)
