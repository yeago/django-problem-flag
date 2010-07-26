import datetime

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ProblemSubscription(models.Model):
	problem = models.ForeignKey('problem.ProblemFlag')
	user = models.ForeignKey('auth.User')

class ProblemFlag(models.Model):
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey('contenttypes.ContentType')
	content_object = generic.GenericForeignKey()
	notes = models.TextField(null=True,blank=True)
	resolved = models.BooleanField(default=False)
	date_added = models.DateTimeField()
	user = models.ForeignKey('auth.User',null=True,blank=True)
	def save(self,*args,**kwargs):
		if not self.date_added:
			self.date_added = datetime.datetime.now()
		super(ProblemFlag,self).save(*args,**kwargs)

