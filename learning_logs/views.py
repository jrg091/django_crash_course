# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

def new_entry(request, topic_id):
    # TODO: validate that there is a topic with given id
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = Topic.objects.get(id = topic_id)
            new_entry.save()
            
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    
    topic = Topic.objects.get(id = topic_id)
    context = { 'topic': topic, 'form': form }
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id = entry_id)
    if request.method != 'POST':
        form = EntryForm(instance = entry)
    else:
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [entry.topic.id]))


    context = { 'entry': entry , 'topic': entry.topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)