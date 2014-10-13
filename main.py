# -*- coding: utf-8 -*-
#
# jQuery File Upload Plugin GAE Python Example 2.2.0
# https://github.com/blueimp/jQuery-File-Upload
#
# Copyright 2011, Sebastian Tschan
# https://blueimp.net
#
# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT
#

from __future__ import with_statement
from google.appengine.api import files, images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import json
import re
import urllib
import webapp2
import httplib
import urllib
#WEBSITE = 'https://blueimp.github.io/jQuery-File-Upload/'
#WEBSITE = '~/apt/miniproject/phase2/jQuery-File-Upload/basic-plus.html'
MIN_FILE_SIZE = 1  # bytes
MAX_FILE_SIZE = 5000000  # bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES
THUMBNAIL_MODIFICATOR = '=s80'  # max width / height


def cleanup(blob_keys):
    blobstore.delete(blob_keys)


class UploadHandler(webapp2.RequestHandler):

    def initialize(self, request, response):
        super(UploadHandler, self).initialize(request, response)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Methods'
        ] = 'OPTIONS, HEAD, GET, POST, PUT, DELETE'
        self.response.headers[
            'Access-Control-Allow-Headers'
        ] = 'Content-Type, Content-Range, Content-Disposition'

    def validate(self, file):
        if file['size'] < MIN_FILE_SIZE:
            file['error'] = 'File is too small'
        elif file['size'] > MAX_FILE_SIZE:
            file['error'] = 'File is too big'
        elif not ACCEPT_FILE_TYPES.match(file['type']):
            file['error'] = 'Filetype not allowed'
        else:
            return True
        return False

    def get_file_size(self, file):
        file.seek(0, 2)  # Seek to the end of the file
        size = file.tell()  # Get the position of EOF
        file.seek(0)  # Reset the file position to the beginning
        return size

    def write_blob(self, data, info):
        blob = files.blobstore.create(
            mime_type=info['type'],
            _blobinfo_uploaded_filename=info['name']
        )
        with files.open(blob, 'a') as f:
            f.write(data)
        files.finalize(blob)
        return files.blobstore.get_blob_key(blob)

    def handle_upload(self):
        results = []
        blob_keys = []
        print "testtesttest"
        print self.request.POST.items()
        for name, fieldStorage in self.request.POST.items():
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = re.sub(
                r'^.*\\',
                '',
                fieldStorage.filename
            )
            result['type'] = fieldStorage.type
            result['size'] = self.get_file_size(fieldStorage.file)
            if self.validate(result):
                blob_key = str(
                    self.write_blob(fieldStorage.value, result)
                )
                blob_keys.append(blob_key)
                result['deleteType'] = 'DELETE'
                result['deleteUrl'] = self.request.host_url +\
                    '/img?key=' + urllib.quote(blob_key, '')
                if (IMAGE_TYPES.match(result['type'])):
                    try:
                        result['url'] = images.get_serving_url(
                            blob_key,
                            secure_url=self.request.host_url.startswith(
                                'https'
                            )
                        )
                        result['thumbnailUrl'] = result['url'] +\
                            THUMBNAIL_MODIFICATOR
                    except:  # Could not get an image serving url
                        pass
                if not 'url' in result:
                    result['url'] = self.request.host_url +\
                        '/img' + blob_key + '/' + urllib.quote(
                            result['name'].encode('utf-8'), '')
            results.append(result)
        return results

    def options(self):
        pass

    def head(self):
        pass

    def post(self):
        if (self.request.get('_method') == 'DELETE'):
            return self.delete()
        results = self.handle_upload()
        result = {'files': results}
        s = json.dumps(result, separators=(',', ':'))
        redirect = self.request.get('redirect')
        if redirect:
            return self.redirect(str(
                redirect.replace('%s', urllib.quote(s, ''), 1)
            ))
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        self.response.write(s)
###############################################################
        stream_id = self.request.get('stream_id')
        print "hahahaha"
        print stream_id
        stream_name = self.request.get('stream_name')
        print stream_name
        page_start = self.request.get('page_start')
        print page_start
        page_end = self.request.get('page_end')
        print page_end
        urls = list()
        for result in results:
            urls.append(result['url'])
        requests = {
            'file': urls,###Use the blobkey
            'stream_id': stream_id
        }
        headers = {"Content-type": "application/json"}
        conn = httplib.HTTPConnection("localhost","8080")
        conn.request("POST", "/api_image_upload", json.dumps(requests), headers)
        responses = conn.getresponse()
        print "hello"
        print page_end
        if results:
           if int(page_end)+len(results) >= 3:
               page_start = 0
               page_end = 2
           else:
               page_start = 0
               page_end = int(page_end) + len(results)
        query_params = {'stream_id':stream_id, 'stream_name':stream_name, 'page_start':page_start, 'page_end':page_end}
        if responses.status == 200:
           self.response.write(s)
           self.redirect('/viewastream?'+urllib.urlencode(query_params))
###############################################################
    def delete(self):
        key = self.request.get('key') or ''
        blobstore.delete(key)
        s = json.dumps({key: True}, separators=(',', ':'))
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        #self.response.write(s)


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, key, filename):
        if not blobstore.get(key):
            self.error(404)
        else:
            # Prevent browsers from MIME-sniffing the content-type:
            self.response.headers['X-Content-Type-Options'] = 'nosniff'
            # Cache for the expiration time:
            self.response.headers['Cache-Control'] = 'public,max-age=%d' % EXPIRATION_TIME
            # Send the file forcing a download dialog:
            self.send_blob(key, save_as=filename, content_type='application/octet-stream')

app = webapp2.WSGIApplication(
    [
        ('/add', UploadHandler),
        ('/img([^/]+)/([^/]+)', DownloadHandler)
    ],
    debug=True
)
