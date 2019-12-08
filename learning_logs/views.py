# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Home page for Learning Logs"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics"""
    context = {'topics': Topic.objects.filter(owner=request.user).order_by('-date_added')}

    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        # Post data submited so we need to handle it
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    
    context = { 'form': form }
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
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

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if entry.topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance = entry)
    else:
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))


    context = { 'entry': entry , 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)