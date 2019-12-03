# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Topic
from .forms import TopicForm

def index(request):
    """Home page for Learning Logs"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics"""
    context = {'topics': Topic.objects.all()}

    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        # Post data submited so we need to handle it
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    
    context = { 'form': form }
    return render(request, 'learning_logs/new_topic.html', context)
