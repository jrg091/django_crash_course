# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Topic(models.Model):
    """ A topic the user is talking bout"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.text

class Entry(models.Model):
    """ A lesson learned about a topic """
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'entries'

    def __unicode__(self):
        if self.text is None:
            return ''
        
        if len(self.text) > 50:
            return self.text[:50] + '...'

        return self.text
            
