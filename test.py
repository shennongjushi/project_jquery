import httplib, urllib
import json
import base64
###Create####usr = binbin##
requests = { 'stream_tag':'1',
             'stream_name':'abc',
             'stream_coverurl':'http://davidfeldmanshow.com/wp-content/uploads/2014/01/dogs-wallpaper.jpg',
             'user_id':'binbin'
           }
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_create_a_stream", json.dumps(requests), headers)
response = conn.getresponse()
print json.loads(response.read())
print "Create a stream usr = binbin\n"
print response.status
print '\n'

###Create###usr = amy##
requests = { 'stream_tag':'1',
             'stream_name':'amy123',
             'stream_coverurl':'http://media1.santabanta.com/full1/Animals/Dogs/dogs-118a.jpg',
             'user_id':'amy'
           }
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_create_a_stream", json.dumps(requests), headers)
response = conn.getresponse()
print "Create a stream usr = amy\n"
print response.status
print '\n'
##Manage####
requests = { 'user_id':'amy'
           }
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_manage", json.dumps(requests), headers)
response = conn.getresponse()
print "Manage user:amy\n"
data = json.loads(response.read()) 
my_stream = data['my_stream']
subscribe_stream = data['subscribe_stream']
print 'my_stream\n'
for i in range(len(my_stream)):
   print 'stream%s:%s' %(i,my_stream[i])
   print '\n'
print 'subscribe_stream\n'
for i in range(len(subscribe_stream)):
   print 'stream%s:%s' %(i,subscribe_stream[i])
   print '\n'

##Manage####
requests = { 'user_id':'binbin'
           }
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_manage", json.dumps(requests), headers)
response = conn.getresponse()
print "Manage user:binbin\n"
data = json.loads(response.read()) 
my_stream = data['my_stream']
subscribe_stream = data['subscribe_stream']
print 'my_stream\n'
for i in range(len(my_stream)):
   print 'stream%s:%s' %(i,my_stream[i])
   print '\n'
print 'subscribe_stream\n'
for i in range(len(subscribe_stream)):
   print 'stream%s:%s' %(i,subscribe_stream[i])
   print '\n'
###view all stream##
requests = {}
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_view_all_streams", json.dumps(requests), headers)
response = conn.getresponse()
data = json.loads(response.read())
stream_id = data['stream_id']
stream_name = data['stream_name']
coverurl = data['coverurl']
print "View all stream\n"
for i in range(len(data['stream_id'])):
   print 'stream_name:' + data['stream_name'][i] + '\n'
   print 'stream_id:' + str(data['stream_id'][i]) + '\n'
   print 'url:' + data['coverurl'][i] + '\n'
   print '\n'

###Upload a image####
for i in range(5):
   key = 'key' + str(i)
   requests = {'file':key,
               'stream_id':str(stream_id[0]),
               'comment':'hello'}
   headers = {"Content-type": "application/json"}
   conn = httplib.HTTPConnection("localhost","8080")
   conn.request("POST", "/api_image_upload", json.dumps(requests), headers)
   response = conn.getresponse()
   print "Image Upload for %s\n" %stream_name[0]
   print response.status
   print '\n'

###view a stream###
requests = { 'id':str(stream_id[0]),
             'page_start':'0',
             'page_end':'2'
           }
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_view_a_stream", json.dumps(requests), headers)
response = conn.getresponse()
data = json.loads(response.read())
url_list = data['url_list']
page_start = data['page_start']
page_end = data['page_end']
print "view a stream %s\n" %stream_name[0]
print 'page_start = %s\n' %page_start
print 'page_end = %s\n' %page_end
for i in range(len(url_list)):
   print 'number%s:%s'%(i,url_list[i])
   print '\n'

###Subscribe a stream####
requests = { 'stream_id':str(stream_id[0]),
             'user_id':'amy'
           }
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_subscribe", json.dumps(requests), headers)
response = conn.getresponse()
print "Subscribe %s" %stream_name[0]
print response.status
print '\n'

##Manage####
requests = { 'user_id':'amy'
           }
headers = {"Content-type": "application/json"}
conn = httplib.HTTPConnection("localhost","8080")
conn.request("POST", "/api_manage", json.dumps(requests), headers)
response = conn.getresponse()
print "Manage user:amy\n"
data = json.loads(response.read()) 
my_stream = data['my_stream']
subscribe_stream = data['subscribe_stream']
print 'my_stream\n'
for i in range(len(my_stream)):
   print 'stream%s:%s' %(i,my_stream[i])
   print '\n'
print 'subscribe_stream\n'
for i in range(len(subscribe_stream)):
   print 'stream%s:%s' %(i,subscribe_stream[i])
   print '\n'

