import cgi
import urllib
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
import webapp2
import json
import base64
from datetime import *
# Each Imag has a Stream Parent
class Imag(ndb.Model):
    pic = ndb.StringProperty()
    comment = ndb.StringProperty()
    imag_id = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)

class Stream(ndb.Model):
    #user = ndb.UserProperty()
    #subscribe_user = ndb.UserProperty()
    name = ndb.StringProperty()
    tag = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add = True)
    coverurl = ndb.StringProperty()
    num_pic = ndb.IntegerProperty()
    view_times = ndb.DateTimeProperty(repeated = True)
    viewers = ndb.IntegerProperty()
    last_date = ndb.DateTimeProperty()

class Webusers(ndb.Model):#Each Webusers xx.key.id() is the user
    mail = ndb.StringProperty()
    my_stream = ndb.StringProperty(repeated = True) #The id of the stream I own
    subscribe_stream = ndb.StringProperty(repeated = True)#The id of the stream I subscribe
    
##Management: take a user id and return two lists of streams
class Manage_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        user_id = requests['user_id']
        user_mail = requests['user_mail']
        user_key = ndb.Key(Webusers,str(user_id))   
        #users = Webusers.query(Webusers.mail==str(user_mail)).fetch()
        #if users:
        #   user = users[0]
        user = user_key.get()
        if not user:
           user = Webusers(id = str(user_id))
           user.mail = str(user_mail)
           #user = Webusers(mail=str(user_mail))
           user.put()
        allusers = Webusers.query().fetch()
        for one in allusers:
           if (str(one.mail) == str(user_mail)) and (str(one.key.id())!= str(user.key.id())):
              for each in one.subscribe_stream:
                 user.subscribe_stream.append(str(each))
              one.key.delete()
        responses = dict()
        responses['my_stream'] = user.my_stream#id
        responses['subscribe_stream'] = user.subscribe_stream#id
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))
class Subscribe_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        stream_id = requests['stream_id']
        user_id = requests['user_id']
        user_mail = requests['mail']
        user = ndb.Key(Webusers,str(user_id)).get()
        #users = Webusers.query(Webusers.mail==str(user_mail)).fetch()
        #if users:
        #    user = users[0]
        if not user:
            user = Webusers(id = str(user_id))
            user.mail=str(user_mail)
            #user = Webusers(mail=str(user_mail))
        if str(stream_id) not in user.subscribe_stream:
            user.subscribe_stream.append(str(stream_id)) 
            user.put()

class Create_a_stream_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        stream_tag = requests['stream_tag']
        stream_name = requests['stream_name']
        stream_coverurl = requests['stream_coverurl']
        user_id = requests['user_id']
        user_mail = requests['mail']
        emails = requests['friend_mails']
        #streams = Stream.query().fetch()
        #flag=0
        #for stream in streams:
        #  print stream.name
        #  if stream_name == stream.name:
        #    print "###############"
        #    self.redirect ('/error')
        #    flag=1
        flag = 0
        if flag == 0:
          stream = Stream(name = stream_name, tag = stream_tag, coverurl = stream_coverurl, num_pic = 0, viewers = 0)
          stream_key = stream.put() ##Return stream_id along with the status code for the manage page and then for view_a_stream which needs a stream_id
          user = ndb.Key(Webusers,str(user_id)).get() 
          #users = Webusers.query(Webusers.mail==str(user_mail)).fetch()
          if user:
              #user = users[0]
              user.my_stream.append(str(stream_key.id()))
              print "@#$!#$!#%!#%!$%!$%"
              user.put()
          else:
              user = Webusers(id = str(user_id))
              user.mail = str(user_mail)
              #user = Webusers(mail=str(user_mail))
              user.my_stream.append(str(stream_key.id()))
              user.put()
          ##################
          if emails[0]:
              for i in range(len(emails)):
                 friends = Webusers.query().fetch()
                 find = 0
                 for friend in friends:
                     if str(friend.mail) == str(emails[i]):
                         find = 1
                         if str(friend.mail)!=str(user_mail):
                            friend.subscribe_stream.append(str(stream_key.id()))
                            friend.put()
                         break
                 if find == 0:
                     print "hellohellohello"
                     new_user = Webusers(mail=str(emails[i]))
                     #print user.user_id()
                     new_user.subscribe_stream.append(str(stream_key.id()))
                     new_user.put()
                         
          ##################
          responses = dict()
          responses['id'] = stream_key.id()
          self.response.headers['Content-Type'] = "application/json"
          self.response.headers['Accept'] = "text/plain"
          self.response.write(json.dumps(responses))

## View a stream: which takes a stream id and a page range and returns a list of URLs to images, and a page range
class View_a_stream_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        stream_id = requests['id']
        stream = ndb.Key(Stream, long(stream_id)).get()
        #Search for the images under the stream_id
        image_query = Imag.query(ancestor = ndb.Key(Stream,long(stream_id))).order(-Imag.date).fetch()
        #if ('page_start' in requests) and ('page_end' in requests):
        #    page_start = requests['page_start']
        #    page_end = requests['page_end']
        #else:
        page_start = requests['page_start']
        page_end = requests['page_end']
        status = ''
        #####Add the view time and remove the time before 1 hour###
        #!!!!!!!!!!!!!!!#####
        if (not page_start) and (not page_end):
            time = datetime.now()
            if stream.view_times:
                stream.view_times = [view_time for view_time in stream.view_times if view_time > (time + timedelta(hours = -1))] 
            stream.view_times.append(time)
            stream.viewers = stream.viewers + 1
            stream.put()
        ###########################################################
        if (not page_start) and (not page_end):
            page_start = 0
            if len(image_query)>3:
                page_end = 2
            else:
                page_end = len(image_query) - 1
        #If the page range is 'less' which means should return <=3 urls
        if int(page_end) + 1 == len(image_query):
            #status = "no_more"
            page_start_more = int(page_start)
            page_end_more = int(page_end)
        else :
            page_start_more = int(page_start) + 3
            if page_start_more + 3 >= len(image_query):
                page_end_more = len(image_query)-1
            else:
                page_end_more = page_start_more + 2
        
        if int(page_start)!=0:
            page_start_less = int(page_start) - 3
            page_end_less = int(page_start)-1
        else:
            status = "no_less"
            page_start_less = int(page_start)
            page_end_less = int(page_end)

        image_urls = list()
        for i in range(int(page_start),int(page_end)+1):
            query_params = {'blob_key':image_query[i].pic, 'stream_id':stream_id}
            image_urls.append('/img?' + urllib.urlencode(query_params))
        responses = dict()
        #print image_urls
        responses['url_list'] = image_urls
        responses['page_start_more'] = page_start_more
        responses['page_start_less'] = page_start_less
        responses['page_end_more'] = page_end_more
        responses['page_end_less'] = page_end_less
        responses['page_start'] = page_start
        responses['page_end'] = page_end
        responses['status'] = status
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))
        #####Add the view time and remove the time before 1 hour###
        
## Image Upload: Takes a stream id and a file
#class Image_Upload_api(webapp2.RequestHandler):
#    def post(self):
#        requests = json.loads(self.request.body)
#        stream_id = requests['stream_id']
#        pic = requests['file']
#        image = Imag(parent = ndb.Key(Stream, long(stream_id)))
#        image.pic = images.resize(pic, 300, 300)
#        image.put()

class Image_Upload_api(webapp2.RequestHandler):
    def post(self):
        responses = json.loads(self.request.body)
        pic = responses['file']#Key of blobstore
        stream_id = responses['stream_id']
        comment = responses['comment']
        if pic:
            imag = Imag(parent = ndb.Key(Stream, long(stream_id)))
            #imag.pic = images.resize(pic,100,100)
            imag.pic = str(pic)
            imag.comment = str(comment)
            imag.put()
            stream = ndb.Key(Stream,long(stream_id)).get()
            stream.num_pic = stream.num_pic + 1
            stream.last_date = datetime.now()
        #print stream.last_date 
            stream.put()

## View all streams: which returns a list of names of streams and their cover images
class View_all_streams_api(webapp2.RequestHandler):
    def post(self):
        streams = Stream.query().order(Stream.date).fetch()
        responses = dict()
        responses['stream_name'] = list()
        responses['stream_id'] = list()
        responses['coverurl'] = list()
        for stream in streams:
            responses['stream_name'].append(stream.name)
            responses['stream_id'].append(stream.key.id())
            responses['coverurl'].append(stream.coverurl)
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

## Search streams: which takes a query string and returns a list of streams(titles and cover image urls) that contain matching text
class Search_streams_api(webapp2.RequestHandler):
    def post(self):
        requests = json.loads(self.request.body)
        query_string = requests['keyword']
        streams = Stream.query().fetch()
        responses = dict()
        responses['names'] = list()
        responses['coverurls'] = list()
        responses['ids'] = list()
        i = 0
        for stream in streams:
            if query_string.lower() in stream.name.lower():
                i = i + 1
                responses['names'].append(stream.name)
                responses['coverurls'].append(stream.coverurl)
                responses['ids'].append(stream.key.id())
                print type(stream.date)
                if i == 5:
                    break
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

## Most viewed Streams: which returns a list of streams sorted by recent access frequency
class Most_viewed_streams_api(webapp2.RequestHandler):
    def viewer_sort(self,l):
        l_len = len(l)
        if l_len < 2:
            return l
        elif l_len == 2:
            if len(l[0].view_times) < len(l[1].view_times):
                l[0],l[1] = l[1],l[0]
            return l
        else:
            for i in range(3):
                for j in range(i+1,l_len):
                    if len(l[j].view_times) > len(l[i].view_times):
                        l[j],l[i] = l[i],l[j]
            return l[:3]
    def post(self):
        responses = dict()
        responses['stream_names'] = list()
        responses['coverurls'] = list()
        responses['stream_ids'] = list()
        responses['last_viewers'] = list()
        streams = Stream.query().fetch()
        time = datetime.now()
        for stream in streams:
            if stream.view_times:
                stream.view_times = [view_time for view_time in stream.view_times if (view_time > time + timedelta(hours = -1))]
        streams = self.viewer_sort(streams)
        for stream in streams:
            responses['stream_names'].append(stream.name)
            responses['coverurls'].append(stream.coverurl)
            responses['stream_ids'].append(stream.key.id())
            responses['last_viewers'].append(len(stream.view_times))
        self.response.headers['Content-Type'] = "application/json"
        self.response.headers['Accept'] = "text/plain"
        self.response.write(json.dumps(responses))

## Reporting requests:
##class Report_requests(webapp2.RequestHandler):
##    def post(self):

application = webapp2.WSGIApplication([
    ('/api_manage',Manage_api),
    ('/api_create_a_stream', Create_a_stream_api),
    ('/api_view_a_stream', View_a_stream_api),
    ('/api_view_all_streams', View_all_streams_api),
    ('/api_image_upload', Image_Upload_api),
    ('/api_search_streams', Search_streams_api),
    ('/api_most_viewed_streams', Most_viewed_streams_api),
    ('/api_subscribe', Subscribe_api),
],debug = True)














