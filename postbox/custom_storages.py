from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
import mimetypes


def store_in_s3(filename,content):
     conn=S3Connection(settings.ACCESS_KEY,settings.PASS_KEY)
     b=conn.get_bucket('thoughtspost')
     mime=mimetypes.guess_type(filename)[0]
     k=Key(b)
     k.key=filename
     k.set_metadata('Content_Type',mime)
     k.set_contents_from_string(content)
     k.set_acl("public-read")