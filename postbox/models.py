from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from  django.utils import *
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import utc
import pytz

# Create your models here.

# class Register(models.Model):
#     # def date_default(self):
#     #     return datetime.now()
#     uname=models.CharField(max_length=50,unique=True)
#     pwd=models.CharField(max_length=25)
#     u_date=models.DateTimeField(null=False, blank=False,default=datetime.now())
#
#     def __unicode__(self):
#         return self.id

class Categories(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE,default="")
    category=models.CharField(max_length=200)
    c_date = models.DateTimeField(null=False, blank=False,default=datetime.now)
    class Meta:
        unique_together = (("owner", "category"),)

    def __unicode__(self):
        return self.category

class Posts(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE,default=" ")
    cid=models.ForeignKey(Categories, on_delete=models.CASCADE)
    title=models.CharField(max_length=200,default="")
    status=models.TextField(default='',null=True)
    image=models.ImageField(upload_to = 'C:/Users/Jyothsna Boyina/PycharmProjects/post/postbox/static/postbox/',null=True,default='')
    p_date = models.DateTimeField(null=False, blank=False,default=datetime.now)

    def __unicode__(self):
        return self.status

class Comments(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=" ")
    pid=models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000, default="")
    cm_date = models.DateTimeField(null=False, blank=False, default=datetime.now)

    def __unicode__(self):
        return self.comment

# class Replies(models.Model):
#     cm_id=models.ForeignKey(Comments, on_delete=models.CASCADE)
#     reply = models.CharField(max_length=1000, default="")
#     r_date = models.DateTimeField(null=False, blank=False,default=datetime.now())
#
#     def __unicode__(self):
#         return self.reply
