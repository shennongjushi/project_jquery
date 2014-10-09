import cgi
import urllib
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api import mail
from datetime import *
from web_api import *
import webapp2
import json
import httplib
import urllib
import web_api
import mimetypes
import base64
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

##92D050
###########Head Template############
HEAD_TEMPLATE = """\
<html>
<head>
   <table>
     <tr>
       <td width=779 colspan=8 valign=top>
         <p style="font-family:Calibri;color:#92D050;font-size:60.0pt"><b>Connex.us</b></p>
       </td>
     </tr>
     <tr>
       <td width=130 valign=top>
         <p><a href="/manage" style="font-family:Calibri;color:%s;font-size:16.0pt;text-decoration:none;">Manage</a></p>
       </td>
       <td width=130 colspan=2 valign=top>
         <p><a href="/create" style="font-family:Calibri;color:%s;font-size:16.0pt;text-decoration:none;">Create</a></p>
       </td>
       <td width=130 valign=top>
         <p><a href="/viewallstreams" style="font-family:Calibri;color:%s;font-size:16.0pt;text-decoration:none;">View</a></p>
       </td>
       <td width=130 valign=top>
         <p><a href="/search" style="font-family:Calibri;color:%s;font-size:16.0pt;text-decoration:none;">Search</a></p>
       </td>
       <td width=130 colspan=2 valign=top>
         <p><a href="/trending" style="font-family:Calibri;color:%s;font-size:16.0pt;text-decoration:none;">Trending</a></p>
       </td>
       <td width=130 valign=top>
         <p><a href="/social" style="font-family:Calibri;color:%s;font-size:16.0pt;text-decoration:none;">Social</a></p>
       </td>
     </tr>
   </table>
</head>
"""

######## For debug#################
global bug
##################################
# Each Imag has a Stream Parent
#class Imag(ndb.Model):
#    pic = ndb.BlobProperty()
#    comment = ndb.StringProperty()
#    imag_id = ndb.IntegerProperty()
#    date = ndb.DateTimeProperty(auto_now_add = True)

#class Stream(ndb.Model):
#    name = ndb.StringProperty()
#    tag = ndb.StringProperty()
#    date = ndb.DateTimeProperty(auto_now_add = True)
#    coverurl = ndb.StringProperty()

#class Webusers(ndb.Model):#Each Webusers xx.key.id() is the user
#    my_stream = ndb.StringProperty(repeated = True) #The id of the stream I own
#    subscribe_stream = ndb.StringProperty(repeated = True)#The id of the stream I subscribe

class Login(webapp2.RequestHandler):
    def get(self):
        log_user = users.get_current_user()
        #if log_user:
        #    self.redirect('/manage')
        #else:
        #    self.redirect(users.create_login_url('/'))
        #self.response.write("""\
        #<html>
        #<head><title>Connex-us</title>
        #</head>
        #<body>
        #<p style="font-family:Calibri;color:black;font-size:50.0pt"><b>Welcome to Connexus</b></p>
        #<p style="font-family:Calibri;color:black;font-size:40.0pt">Share the world!</p>
        #<a href ="%s">
        #<image src ="https://developers.google.com/accounts/images/sign-in-with-google.png">
        #</a>
        #</body>
        #</html> 
        #"""
        #%(users.create_login_url('/manage')))
        url=users.create_login_url('/manage')
        template_value = {
            'url':url
        }
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_value))

class Error(webapp2.RequestHandler):
  def get(self):
#        grey = '#D0CECE'
#        blue = '#2E75B6'
#        self.response.write(HEAD_TEMPLATE %(blue,grey,blue,blue,blue,blue))
        info = self.request.get('info')
#        if info == 'same_name':
#            self.response.write("""\
#            <body>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">Error:you tried to create a new stream</p>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">whose name is the same as an existing stream</p>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">operation did not complete</p>
#            </body>
#            </html>
#            """)
#        elif info == 'no_name':
#            self.response.write("""\
#            <body>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">Error:you tried to create a new stream</p>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">But the name is empty</p>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">operation did not complete</p>
#            </body>
#            </html>
#            """)
#        elif info =='wrong_email':
#            self.response.write("""\
#            <body>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">Error:Wrong Email</p>
#            <p style="font-family:Calibri;color:red;font-size:16.0pt">operation did not complete</p>
#            </body>
#            </html>
#            """)
        template_value = {
            'info':info
        }
        template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(template.render(template_value))

#############Create##############
class Create(webapp2.RequestHandler):
    def get(self):
      user = users.get_current_user()
      if not user:
        self.redirect(users.create_login_url('/manage'))
      template_value = dict()
      template = JINJA_ENVIRONMENT.get_template('create.html')
      self.response.write(template.render(template_value))
        #grey = '#D0CECE'
        #blue = '#2E75B6'
        #self.response.write(HEAD_TEMPLATE %(blue,grey,blue,blue,blue,blue))
#        self.response.write("""\
#      	<body>
#        </br>
#        <form enctype = "multipart/form-data" method = "post">
#        <table>
#        <tr>
#        <td>
#        <div stype="font-family:Calibri;color:black;font-size:20.0pt"><label><b>Name Your Stream</b></label></div>
#        <div><textarea name="stream_name" rows="2" cols="60"></textarea></div>
#        <div stype="font-family:Calibri;color:black;font-size:20.0pt"><label><b>Add subscribers</b></label></div>
#        <div><textarea name="email" rows="4" cols="60" placeholder="Seperate emails by ','"></textarea></div>
#        <div><textarea name="message" rows="4" cols="60" placeholder="Optional message for invite"></textarea></div>
#        </td>
#        <td>
#        <div stype="font-family:Calibri;color:black;font-size:20.0pt"><label><b>Tag Your Stream</b></label></div>
#        <div><textarea name="stream_tag" rows="4" cols="60" placeholder="#LucknowChristianCollege,$1985, #AdnansFriends,#FB:schools.india.LCC"></textarea></div>
#        <div></br><div>
#        <div><label><b>URL to cover image(Can be empty)</b></label></div>
#        <div><textarea name="cover_url" rows="3" cols="60" placeholder="http://flickr.com/tiger-image.png"></textarea></div>
#        <div><input type="submit" values="Create Submit"></div>
#        </td>
#        </tr>
#        <table>
#        </form>
#        </body>
#        </html>
#""")
    def post(self):
        name = self.request.get('stream_name')
        if not name:
            self.redirect('/error?info=no_name')
        else:
            flag = 0
            streams = Stream.query().fetch()
            for stream in streams:
               if name == stream.name:
                   flag = 1
                   self.redirect ('/error?info=same_name')
            if flag == 0:
               tag = self.request.get('stream_tag')
               coverurl = self.request.get('cover_url')
               friendmail=self.request.get('email')
               message=self.request.get('message')
               message = message + '\n' + 'link:' + 'connex-us-2014.appspot.com'
               friendmail=friendmail.strip().strip(',')
               friendmail=friendmail.split(',')
               sender = users.get_current_user()
               if sender is None:
                  flag = 1
                  self.redirect(users.create_login_url('/create'))
               elif friendmail[0]:
                  for i in range(len(friendmail)):
                     friendmail[i]=friendmail[i].strip()
                     if '@' not in friendmail[i]:
                        flag = 2
                        self.redirect('/error?info=%s' %"wrong_email")
                     else:
                        mail.send_mail(sender.email(), friendmail[i], "Connex Subscribe Inviation", message)
	       if flag == 0:
                  user_id = sender.user_id()
                  requests = dict()
                  requests['stream_tag'] = str(tag)
                  requests['stream_name'] = str(name)
                  requests['stream_coverurl'] = str(coverurl)
                  requests['user_id'] = str(user_id)
                  requests['mail'] = str(sender.email())
                  requests['friend_mails'] = friendmail
                  headers = {"Content-type": "application/json", "Accept": "text/plain"}
                  conn = httplib.HTTPConnection("localhost","8080")
                  conn.request("POST", "/api_create_a_stream", json.dumps(requests), headers)
                  response = conn.getresponse()
                  if response.status == 200:
                      self.redirect('/manage')

class Manage(webapp2.RequestHandler):
   def get(self):
        user = users.get_current_user()
        url = ''
        url_linktext = ''
        my_stream_entity = list()
        subscribe_stream_entity = list()
        if not user:
           self.redirect(users.create_login_url('/manage'))
        else:
           url = users.create_logout_url('/')
           url_linktext = 'Logout'
           #grey = '#D0CECE'
           #blue = '#2E75B6'
           #self.response.write(HEAD_TEMPLATE %(grey,blue,blue,blue,blue,blue))
#           self.response.write("""\
#            <body>
#            </br>
#            <table>
#            <tr>
#            <td width=130 valign=top>
#            <p style="font-family:Calibri;color:#FFC000;font-size:14.0pt"><i>Hello,%s</i></p>
#            </td>
#            <td></td>
#            <td><a href="%s">%s</a></td>
#            </tr>
#            </table>
#            </br>
#            <form action="/delete_my" enctype = "multipart/form-data" method ="post">
#            <table>
#            <tr>
#            <td width=779 colspan=8 valign=top>
#            <p style="font-family:Calibri;color:black;font-size:18.0pt"><b>Stream I own</b></p>
#            </td>
#            </tr>
#            <tr></tr>
#            <tr></tr>
#            <tr>
#            <td width=195 colspan=2 valign=top>
#            <p style="font-family:Calibri;color:black;font-size:12.0pt">Name</p>
#            </td>
#            <td width=195 colspan=2 valign=top>
#            <p style="font-family:Calibri;color:black;font-size:12.0pt">Last New Picture</p>
#            </td>
#            <td width=195 colspan=2 valign=top>
#            <p style="font-family:Calibri;color:black;font-size:12.0pt">Number of Pictures</p>
#            </td>
#            <td width=195 colspan=2 valign=top>
#            <p style="font-family:Calibri;color:black;font-size:12.0pt">Views</p>
#            </td>
#            <td width=195 colspan=2 valign=top>
#            <p style="font-family:Calibri;color:black;font-size:12.0pt">Delete</p>
#            </td>
#            </tr>
#           """ %(user.nickname(),url,url_linktext))
           requests = {
               'user_id': str(users.get_current_user().user_id()),
               'user_mail': str(users.get_current_user().email())
           }	
           headers = {"Content-type": "application/json", "Accept": "text/plain"}
           conn = httplib.HTTPConnection("localhost","8080")
           conn.request("POST", "/api_manage", json.dumps(requests), headers)
           responses = conn.getresponse()
           if responses.status == 200:
               data = json.loads(responses.read())
               my_stream = data['my_stream']
               subscribe_stream = data['subscribe_stream']
               for stream in my_stream:
                   my_stream_entity.append(ndb.Key(Stream,long(stream)).get())
               #if my_stream_entity:
               #    print my_stream_entity[0].key.id()
               for stream in subscribe_stream:
                   subscribe_stream_entity.append(ndb.Key(Stream,long(stream)).get())
                   #if stream_entity.num_pic != 0:
                   #    update_date = str(stream_entity.last_date.date())
                   #else:
                   #    update_date = str(stream_entity.date.date())
#                   self.response.write("""\
#                    <tr>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt"><a href="/viewastream?stream_id=%s&stream_name=%s">%s</a></p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt">%s</p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt">%s</p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt">%s</p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt"><input type="checkbox" name="del" value ="%s"></p>
#                    </td>
#                   </tr>
#                   """
#                    %(stream,stream_entity.name,stream_entity.name,update_date,stream_entity.num_pic,stream_entity.viewers,stream_entity.key.id()))
#               self.response.write("""\
#                   <tr>
#                   <td width=195 colspan=2 valign=top>
#                   <input type ="submit" value="Delete Checked">
#                   </tr>
#                   </table>
#                   </form>
#                 </br>
#               """)
#               self.response.write("""\
#               <form action="/delete_subscribe" enctype = "multipart/form-data" method ="post">
#               <table>
#               <tr>
#               <td width=779 colspan=8 valign=top>
#               <p style="font-family:Calibri;color:black;font-size:18.0pt"><b>Stream I subscribe to</b></p>
#               </td>
#               </tr>
#               <tr></tr>
#               <tr></tr>
#               <tr>
#               <td width=195 colspan=2 valign=top>
#               <p style="font-family:Calibri;color:black;font-size:12.0pt">Name</p>
#               </td>
#               <td width=195 colspan=2 valign=top>
#               <p style="font-family:Calibri;color:black;font-size:12.0pt">Last New Picture</p>
#               </td>
#               <td width=195 colspan=2 valign=top>
#               <p style="font-family:Calibri;color:black;font-size:12.0pt">Number of Pictures</p>
#               </td>
#               <td width=195 colspan=2 valign=top>
#               <p style="font-family:Calibri;color:black;font-size:12.0pt">Views</p>
#               </td>
#               <td width=195 colspan=2 valign=top>
#               <p style="font-family:Calibri;color:black;font-size:12.0pt">Unsubscribe</p>
#               </td>
#               </tr>
#               """ )
#               for stream in subscribe_stream:
#                   stream_entity = ndb.Key(Stream,long(stream)).get()
#                   if stream_entity:
#                       if stream_entity.num_pic != 0:
#                           update_date = str(stream_entity.last_date.date())
#                       else:
#                           update_date = str(stream_entity.date.date())
#                       self.response.write("""\
#                   <tr>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt"><a href="/viewastream?stream_id=%s&stream_name=%s">%s</a></p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt">%s</p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt">%s</p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt">%s</p>
#                    </td>
#                    <td width=195 colspan=2 valign=top>
#                    <p style="font-family:Calibri;color:black;font-size:12.0pt"><input type="checkbox" name="del" value ="%s"></p>
#                    </td>
#                   </tr>
#                   """ 
#                   %(stream,stream_entity.name,stream_entity.name,update_date,stream_entity.num_pic,stream_entity.viewers,stream_entity.key.id()))
#               self.response.write("""\
#                   <tr>
#                   <td width=195 colspan=2 valign=top>
#                   <input type ="submit" value="Unsubscribe Checked Streams">
#                   </tr>
#                   </table>
#                   </form>
#                 </br>
#               """)
#               self.response.write('</body></html>')

        template_values = {
            'my_stream': my_stream_entity,
            'subscribe_stream': subscribe_stream_entity,
            'url': url,
            'url_linktext': url_linktext,
            'user':user
        }

        template = JINJA_ENVIRONMENT.get_template('manage.html')
        self.response.write(template.render(template_values))

class Delete_my(webapp2.RequestHandler):
    def post(self):
        delete_id = self.request.get_all('del')
        #users = Webusers.query(mail==str(users.get_current_user().email())).fetch()
        #user = users[0]
        user = ndb.Key(Webusers,str(users.get_current_user().user_id())).get()
        for i in delete_id:
           stream = ndb.Key(Stream, long(i)).get()
           ################
           image_query = Imag.query(ancestor=ndb.Key(Stream,long(i)))
           for image in image_query:
               blobstore.delete(urllib.unquote(image.pic))
               image.key.delete()
           ################ 
           stream.key.delete()
           user.my_stream.remove(str(i))
           alluser=Webusers.query().fetch()
           for one_user in alluser:
             if i in one_user.subscribe_stream:
               one_user.subscribe_stream.remove(str(i))
               one_user.put()
        user.put()
        self.redirect('/manage')
           
        
class Delete_subscribe(webapp2.RequestHandler):
    def post(self):
        delete_id = self.request.get_all('del')
        #users = Webusers.query(mail==str(users.get_current_user().email())).fetch()
        #user = users[0]
        user = ndb.Key(Webusers,str(users.get_current_user().user_id())).get()
        for i in delete_id:
           user.subscribe_stream.remove(str(i))
        user.put()
        self.redirect('/manage')

class View_all_stream(webapp2.RequestHandler):
    def get(self):
        #grey = '#D0CECE'
        #blue = '#2E75B6'
        #self.response.write(HEAD_TEMPLATE %(blue,blue,grey,blue,blue,blue))
        #self.response.write('<body><p style="font-family:Calibri;color:black;font-size:36.0pt"><b>View All Streams</b></p>')
  
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost","8080")
        conn.request("POST", "/api_view_all_streams","", headers)
        responses = conn.getresponse()
        #print responses.status
        data = json.loads(responses.read())
        stream_names = data['stream_name']
        stream_ids = data['stream_id']
        stream_coverurls = data['coverurl']
       # print stream_coverurls
        if len(stream_names)%4!=0:
            rows = len(stream_names)/4 + 1
        else:
            rows = len(stream_names)/4
        j = -4
        print "row=%s" %rows
        stream_coverurls_str = list()
        stream_len = len(stream_names)
        for stream in stream_coverurls:
          stream_coverurls_str.append(str(stream))
        template_values = {
            'stream_names': stream_names,
            'stream_ids': stream_ids,
            'stream_coverurls': stream_coverurls_str,
            'rows': rows,
            'stream_len':stream_len,
        }

        template = JINJA_ENVIRONMENT.get_template('view_all.html')
        self.response.write(template.render(template_values))
#        for i in range(rows):
#            self.response.write('<table><tr>')
#            if i!=rows-1 or (i==rows-1 and len(stream_names)%4==0):##Not the last row
#                for m in range(4):
#                    self.response.write("""\
#                    <td>
#                    <div class="c_img"><a href = "/viewastream?stream_id=%s&stream_name=%s">
#                    <img src="%s" width="200px" height="200px" 
#                    style=" border:3;padding:8;border-style:dotted;color=#990000"></a>
#                    <div><a href ="/viewastream?stream_id=%s&stream_name=%s" class="c_words" 
#                    style="font-family:Calibri;color:black;font-size:20.0pt;text-decoration:none">%s
#                    </a></div></div>
#                    <style>
#                    .c_img{position:relative;}
#                    .c_words{position:absolute;width:200px;height:30px;top:95px;left:11px;
#                    text-align:center;filter:alpha(opacity=60);opacity:0.6;background:white}
#                    </style>
#                    </td>
#                    <td></td>
#                    <td></td>
#                    <td></td>
#                    """
#                    %(stream_ids[j+m],stream_names[j+m],str(stream_coverurls[j+m]),stream_ids[j+m],stream_names[j+m],stream_names[j+m]))
#	 	j = j + 4
#            else:
#                for m in range(len(stream_names)%4):
#                    self.response.write("""\
#                    <td>
#                    <div class="c_img"><a href = "/viewastream?stream_id=%s&stream_name=%s">
#                    <img src="%s" width="200px" height="200px" 
#                    style=" border:3;padding:8;border-style:dotted;color=#990000"></a>
#                    <div><a href ="/viewastream?stream_id=%s&stream_name=%s" class="c_words" 
#                    style="font-family:Calibri;color:black;font-size:20.0pt;text-decoration:none">%s
#                    </a></div></div>
#                    <style>
#                    .c_img{position:relative;}
#                    .c_words{position:absolute;width:200px;height:30px;top:95px;left:11px;
#                    text-align:center;filter:alpha(opacity=60);opacity:0.6;background:white}
#                    </style>
#                    </td>
#                    <td></td>
#                    <td></td>
#                    <td></td>
#                    """
#                    %(stream_ids[j+m],stream_names[j+m],str(stream_coverurls[j+m]),stream_ids[j+m],stream_names[j+m],stream_names[j+m]))
#                
#            self.response.write('</tr></table></br>')
#        self.response.write('</body></html>')


class View_a_stream(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = ''
        url_linktext = ''
        if not user:
           self.redirect(users.create_login_url(self.request.uri))
        else:
           url = users.create_logout_url('/')
           url_linktext = 'Logout'
#           grey = '#D0CECE'
#           blue = '#2E75B6'
#           self.response.write(HEAD_TEMPLATE %(blue,blue,grey,blue,blue,blue))
           stream_name = self.request.get('stream_name')
           stream_id = self.request.get('stream_id')
           page_start = self.request.get('page_start')
           page_end = self.request.get('page_end')
           requests = {
               'id': str(stream_id),
               'page_start':str(page_start),
               'page_end':str(page_end),
           }
           headers = {"Content-type": "application/json", "Accept": "text/plain"}
           conn = httplib.HTTPConnection("localhost","8080")
           conn.request("POST", "/api_view_a_stream", json.dumps(requests), headers)
           responses = conn.getresponse()
           print responses.status
           data = json.loads(responses.read())
           urls = data['url_list']
           page_start_more = data['page_start_more']
           page_end_more = data['page_end_more']
           page_start_less = data['page_start_less']
           page_end_less = data['page_end_less']
           page_start = data['page_start']
           page_end = data['page_end']
           status = data['status']
#           self.response.write('<body><p style="font-family:Calibri;color:black;font-size:30.0pt"><b>%s</b></p><table>' %stream_name)
#           for url in urls: 
#               self.response.write('<td><img src=%s width="200px" height="200px"></img></td>' %url)
#               self.response.write('<td></td><td></td>')
#           self.response.write('</table>')
#           #######More button##########
#           self.response.write('<a href="/viewastream?stream_id=%s&stream_name=%s&page_start=%s&page_end=%s"><input type ="button" value=%s></a></tr>' %(stream_id,stream_name,page_start_more,page_end_more,"more"))
           user = ndb.Key(Webusers,str(users.get_current_user().user_id())).get()
#           #users = Webusers.query(mail==str(users.get_current_user().email())).fetch()
#           #user = users[0]
#           #######Less button#########
#           if status != 'no_less':
#               self.response.write('<a href="/viewastream?stream_id=%s&stream_name=%s&page_start=%s&page_end=%s"><input type ="button" value=%s></a>' %(stream_id,stream_name,page_start_less,page_end_less,"less"))
########   ###################################################################################
#	   				Change to Blobstore		                  #
########   ###################################################################################
           upload_url = blobstore.create_upload_url('/add?stream_id=%s&stream_name=%s&page_start=%s&page_end=%s' %(stream_id,stream_name,page_start,page_end))
           #if user and (str(stream_id) in user.my_stream):
#           self.response.write("""\
#               <form action="%s" enctype = "multipart/form-data" method="post">
#               <table>
#               <p style="font-family:Calibri;font-size:20.0pt;">Add an Image</p>
#               <tr><input type = "file" name = "img"/></tr></br>
#               <tr><input type="text" name="comment" placeholder="comments"/></tr></br></br>
#               <tr><input type = "submit" value = "Upload file"></tr>
#               </table>
#               </form>
#                """ %upload_url)
#           if (not user) or (str(stream_id) not in user.my_stream):
#               self.response.write("""\
#               <form action="/subscribe?stream_id=%s&stream_name=%s"  method="post">
#               <div><input type = "submit" value = "subscribe"></div>
#               </form>
#               </hr>
#               """%(stream_id,stream_name))
#           #global bug
#           #self.response.write("<h1>%s</h1>" %bug)
#           self.response.write('</body></html>')
        template_values = {
            'stream_name': stream_name,
            'stream_id': stream_id,
            'stream_id_str':str(stream_id),
            'page_start':page_start,
            'page_end':page_end,
            'urls':urls,
            'page_start_more':page_start_more,
            'page_end_more':page_end_more,
            'page_start_less': page_start_less,
            'page_end_less':page_end_less,
            'status':status,
            'upload_url':upload_url,
            'user':user
        }

        template = JINJA_ENVIRONMENT.get_template('view_one.html')
        self.response.write(template.render(template_values))

class Subscribe(webapp2.RequestHandler):
   def post(self):
       if users.get_current_user():
           stream_id = self.request.get('stream_id')
           stream_name = self.request.get('stream_name')
           requests = {
                'stream_id': str(stream_id),
                'user_id':str(users.get_current_user().user_id()),
                'mail':str(users.get_current_user().email())
           }
           headers = {"Content-type": "application/json"}
           conn = httplib.HTTPConnection("localhost","8080")
           conn.request("POST", "/api_subscribe", json.dumps(requests), headers)
           responses = conn.getresponse()
           self.redirect("/viewastream?stream_id=%s&stream_name=%s"%(stream_id,stream_name))
       else :
           self.redirect(users.create_login_url(self.request.uri))
       
######################################################################################
#                          Blobstore Download Handler                                #
######################################################################################
class Image_Show(blobstore_handlers.BlobstoreDownloadHandler):
   def get(self):
       blob_key = self.request.get('blob_key')
       blob_info = blobstore.BlobInfo.get(str(urllib.unquote(blob_key)))
       self.send_blob(blob_info)

######################################################################################
#                          Blobstore Upload Handler                                  #
######################################################################################
class Image_Add(blobstore_handlers.BlobstoreUploadHandler):
   def post(self):
       stream_id = self.request.get('stream_id')
       stream_name = self.request.get('stream_name')
       page_start = self.request.get('page_start')
       page_end = self.request.get('page_end')
       comment = self.request.get('comment')
       upload_files = self.get_uploads('img')
       if upload_files:
           blob_info = upload_files[0]
           blob_key = str(blob_info.key())
       else:
           blob_key = ''
       requests = {
            'file': blob_key,###Use the blobkey
            'stream_id': stream_id,
            'comment': comment
       }
       headers = {"Content-type": "application/json"}
       conn = httplib.HTTPConnection("localhost","8080")
       conn.request("POST", "/api_image_upload", json.dumps(requests), headers)
       responses = conn.getresponse()
       #global bug
       #bug = responses.status
       if upload_files:
           if int(page_end)+1 >= 3:
               page_start = 0
               page_end = 2
           else:
               page_start = 0
               page_end = int(page_end) + 1
       query_params = {'stream_id':stream_id, 'stream_name':stream_name, 'page_start':page_start, 'page_end':page_end}
       if responses.status == 200:
           self.redirect('/viewastream?'+urllib.urlencode(query_params))
      ################for debug##################
       else:
           self.redirect('/debug?status=%s' %responses.status)

class Search(webapp2.RequestHandler):
    def get(self):
#        grey = '#D0CECE'
#        blue = '#2E75B6'
#        self.response.write(HEAD_TEMPLATE %(blue,blue,blue,grey,blue,blue))
#        self.response.write("""\
#             </br>
#             <body>
#             <form action = "/search" enctype = "multipart/form-dat" method = "get">
#               <div><input type = "text" name = "keyword" placeholder="Keyword" style="font-family:Calibri;color:black;font-size:20.0pt;height:25pt;width:200pt;"></div>
#               <div><input type = "submit" values = "Search"></div>
#            </form>""")
        keyword = self.request.get('keyword')
        stream_names = list()
        stream_coverurls = list()
        stream_coverurls_str = list()
        stream_ids = list()
        if keyword:
            requests = {'keyword':str(keyword)}
            headers = {"Content-type": "application/json", "Accept": "text/plain"}
            conn = httplib.HTTPConnection("localhost","8080")
            conn.request("POST", "/api_search_streams", json.dumps(requests), headers)
            responses = conn.getresponse()
            data = json.loads(responses.read())
            stream_names = data['names']
            stream_coverurls = data['coverurls']
            for url in stream_coverurls:
              stream_coverurls_str.append(str(url))
            stream_ids = data['ids']
#            if stream_names:
#                self.response.write('<p style="font-family:Calibri;color:black;font-size:16.0pt">%d results for %s, click on an image to view stream </p>' %(len(stream_names),keyword))
#                for i in range(0,len(stream_names)):
#                    self.response.write("""\
#                    <div class="c_img"><a href = "/viewastream?stream_id=%s&stream_name=%s">
#                    <img src="%s" width="200px" height="200px" 
#                    style=" border:3;padding:8;border-style:dotted;color=#990000"></a>
#                    <div><a href ="/viewastream?stream_id=%s&stream_name=%s" class="c_words" 
#                    style="font-family:Calibri;color:black;font-size:20.0pt;text-decoration:none">%s
#                    </a></div></div>
#                    <style>
#                    .c_img{position:relative;}
#                    .c_words{position:absolute;width:200px;height:30px;top:95px;left:11px;
#                    text-align:center;filter:alpha(opacity=60);opacity:0.6;background:white}
#                    </style>
#                    </br>
#                    """
#                    %(stream_ids[i],stream_names[i],str(stream_coverurls[i]),stream_ids[i],stream_names[i],stream_names[i]))
#            else:
#                self.response.write('<p style="font-family:Calibri;color:black;font-size:16.0pt">No Result matchs string %s</p>' %keyword)
#        self.response.write('</body></html>')
        template_values = {
            'keyword': keyword,
            'stream_names':stream_names,
            'stream_coverurls':stream_coverurls_str,
            'stream_ids':stream_ids,
            'stream_names_len':len(stream_names)
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

class Social(webapp2.RequestHandler):
    def get(self):
        grey = '#D0CECE'
        blue = '#2E75B6'
        self.response.write(HEAD_TEMPLATE %(blue,blue,blue,blue,blue,grey))
        self.response.write('</html>')

global count
count=0
global rate
rate=0
global check
check = ['checked','','','']
#global message
#message = ""
class Trending(webapp2.RequestHandler):
    def get(self):
#        grey = '#D0CECE'
#        blue = '#2E75B6'
#        self.response.write(HEAD_TEMPLATE %(blue,blue,blue,blue,grey,blue))
#        self.response.write('<body><p style="font-family:Calibri;color:black;font-size:36.0pt"><b>Top 3 Trending Streams</b></p>')
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost","8080")
        conn.request("POST", "/api_most_viewed_streams","", headers)
        responses = conn.getresponse()
        data = json.loads(responses.read())
        stream_names = data['stream_names']
        coverurls = data['coverurls']
        stream_ids = data['stream_ids']
        last_viewers = data['last_viewers']
#        self.response.write('<table><tr>')
        coverurls_str = list()
        for url in coverurls:
          coverurls_str.append(str(url))
        #global message
        #message = ""
        #for i in range(len(stream_names)):
        #    message = message+stream_names[i]+":"+str(last_viewers[i])+"\n"
#        for i in range(len(stream_names)):
#            self.response.write("""\
#            <td>
#            <div class="c_img"><a href = "/viewastream?stream_id=%s&stream_name=%s">
#            <img src="%s" width="200px" height="200px" 
#            style=" border:3;padding:8;border-style:dotted;color=#990000"></a>
#            <div><a href ="/viewastream?stream_id=%s&stream_name=%s" class="c_words" 
#            style="font-family:Calibri;color:black;font-size:20.0pt;text-decoration:none">%s
#            </a></div></div>
#            <style>
#            .c_img{position:relative;}
#            .c_words{position:absolute;width:200px;height:30px;top:95px;left:11px;
#            text-align:center;filter:alpha(opacity=60);opacity:0.6;background:white}
#            </style>
#            <div><p style="font-family:Calibri;color:black;font-size:18.0pt">%d views in past hour
#            </p></div>
#            </td>
#            <td></td>
#            <td></td>
#            <td></td>
#            """
#            %(stream_ids[i],stream_names[i],str(coverurls[i]),stream_ids[i],stream_names[i],stream_names[i],last_viewers[i]))
        
        rate_now = self.request.get('rate')
        global check
        if rate_now:
            if rate_now == '0':
               check=['checked','','','']
            elif rate_now == '1':
               check=['','checked','','']
            elif rate_now == '12':
               check=['','','checked','']
            elif rate_now == '288':
               check=['','','','checked']

#        self.response.write("""
#          <td><form  method = "post">
#          Current Rate<br>
#          <input type="radio" name ="rate" value="0" %s>No reprots<br>
#          <input type="radio" name ="rate" value="1" %s>Every 5 minutes<br>
#          <input type="radio" name ="rate" value="12" %s>Every 1 hour<br>
#          <input type="radio" name ="rate" value="288" %s>Every day<br>
#          <input type="submit" value="Update Rate">
#          </form>
#          </td></table>
#          </body>
#          </html>
#          """
#          %(check[0],check[1],check[2],check[3]))
        template_values = {
            'stream_names': stream_names,
            'stream_names_len':len(stream_names),
            'coverurls':coverurls_str,
            'stream_ids':stream_ids,
            'last_viewers':last_viewers,
            'check':check
        }

        template = JINJA_ENVIRONMENT.get_template('trend.html')
        self.response.write(template.render(template_values))
    def post(self):
      ########
      global count
      count = 0
      ########
      global rate
      rate = self.request.POST.get('rate')
      self.redirect('/trending?rate=%s' %rate)

class Count_job(webapp2.RequestHandler):
  def get(self):
    global count
    count = count+1
    print count
    global rate
    print rate
    #global message
    #print message
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost","8080")
    conn.request("POST", "/api_most_viewed_streams","", headers)
    responses = conn.getresponse()
    data = json.loads(responses.read())
    stream_names = data['stream_names']
    coverurls = data['coverurls']
    stream_ids = data['stream_ids']
    last_viewers = data['last_viewers']
    
    if int(rate)!=0:
        if int(count)%int(rate)==0:
            message = "Report of last one hour:\n"
            for i in range(len(stream_names)):
                rank = str(i+1)
                message = message+'rank'+ rank +':  '+stream_names[i]+":"+str(last_viewers[i])+"\n"
            mail.send_mail("fubinbinole@gmail.com","ragha@utexas.edu","Most_View_Pics",message)
            mail.send_mail("fubinbinole@gmail.com","natviv@cs.utexas.edu","Most_View_Pics",message)

class Debug(webapp2.RequestHandler):
    def get(self):
        bug = self.request.get('status')
        self.response.write("<html><h1>%s</h1></html>" %bug)
        

application = webapp2.WSGIApplication([
    ('/',Login),
    ('/count',Count_job),
    ('/create', Create),
    ('/error', Error),
    ('/manage', Manage),
    ('/viewastream',View_a_stream),
    ('/viewallstreams',View_all_stream),
    ('/img',Image_Show),
    ('/add',Image_Add),
    ('/debug',Debug),
    ('/search',Search),
    ('/trending', Trending),
    ('/social', Social),
    ('/subscribe', Subscribe),
    ('/delete_my', Delete_my),
    ('/delete_subscribe',Delete_subscribe),

],debug = True)














