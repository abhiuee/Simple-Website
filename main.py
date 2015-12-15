
import os

import jinja2
import webapp2
import urllib2
from google.appengine.ext import ndb
import httplib
import json
from google.appengine.api import urlfetch

urlfetch.set_default_fetch_deadline(600)

# Set up jinja environment
template_dir = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)
# Google API 
google_url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDhG7IcKerUStbsVkV6tEqqjMNMpLcR0Gc&sensor=false&latlng="
# Create global variables for database and current user
comments_database = 'comments'
current_user = "Anonymous"

def get_city_country(latlng):
    """ get city and country from latitude and longitude"""
    url = google_url + latlng
    print url
    error_code = 1;
    try:
        content = urllib2.urlopen(url).read()
    except (urllib2.URLError, httplib.HTTPException):
        error_code = 2
        return None, None
    city = None
    country = None
    if content:
        data = json.loads(content)
        if data:
            error_code = -1
            if data["status"] == "OK":
                error_code = -2
                d = data["results"][0]["address_components"]
                if d:
                    error_code = -3
                    for tup in d:
                        if "locality" in tup["types"]:
                            error_code = 0
                            city = tup["long_name"]
                        elif "country" in tup["types"]:
                            error_code = 0
                            country = tup["short_name"]
            else:
                city = str(data)
                error_code = -4             
    return city, country, error_code


    return None, None

def valid_user_name(user_name):
    """ Validate user name. username with digits and alphabets allowed """
    for ch in user_name:
        if not (ch.isdigit() or ch.isalpha()):
            print "Return False"
            return False
    return True

def comments_key(database=comments_database):
    """Constructs a Datastore key for a comments entity.
    """
    return ndb.Key('Comments', database)

class Comment(ndb.Model):
    """A main model for representing an individual comment entry."""
    user = ndb.StringProperty(indexed = False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    city = ndb.StringProperty(indexed = False)
    country = ndb.StringProperty(indexed = False)


class Handler(webapp2.RequestHandler):
    """ Main Handler class to render all the HTML pages """
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    """ Handler class for "/*" documents """
    def get(self):
        comments_query = Comment.query(
            ancestor=comments_key(comments_database)).order(-Comment.date)
        number_of_comments = 10
        comments_list = comments_query.fetch(number_of_comments)
        invalid_comment = self.request.get("invalid_comment")
        error_code = self.request.get("error")
        global current_user
        if current_user == "Anonymous":
            user_status = "Login"
        else:
            user_status = "Logout"

        self.render("my_first.html", user_status = user_status, user_name = current_user, comments_list = comments_list, invalid_comment = invalid_comment, error_code = error_code)

class LoginPageLoader(Handler):
    """ Class for /login """
    def get(self):
        self.render("login.html", text = "")

    def post(self):
        user_name = self.request.get("user_name")
        if not user_name:
            self.render("login.html", text = "Please enter a name in the text box")
        elif valid_user_name(user_name):
            global current_user
            current_user = user_name
            self.redirect("/")
        else:
            self.render("login.html", text = "Please enter a valid name in the text box. A valid name is a combination of digits and alphabets")


class PostPageLoader(Handler):
    """ Class for /post """
    def post(self):
        comments_data = Comment(parent=comments_key(comments_database))
        comments_data.user = current_user
        comments_data.content = self.request.get("content")
        locate = self.request.get("location_tag")
        error_code = 0;
        if locate != "":
            city, country, error_code = get_city_country(locate)
            comments_data.city = city
            comments_data.country = country
        if comments_data.content and comments_data.content.strip():
            comments_data.put()
            if error_code != 0:
                url = "/?error="+str(error_code)+"&latlng="+locate
            else:
                url= "/"
            url = url+"#comments"
            self.redirect(url)
        else:
            if error_code != 0:
                url = "/?error="+str(error_code)+"&"
            else:
                url = "/?"
            url = url+"invalid_comment=true#comments"
            self.redirect(url)

class LogOutPageLoader(Handler):
    """ Class for /logout """
    def post(self):
        global current_user
        current_user = "Anonymous"
        self.redirect("/")

app = webapp2.WSGIApplication([("/", MainPage), ("/login", LoginPageLoader), ("/post", PostPageLoader), ("/logout", LogOutPageLoader)])
