from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from learning_logs.models import Topic, Entry
from learning_logs.forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404


def index(request):
    return render(request, 'index.txt')


@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    return render(request, 'topics.txt', {'topics': topics})


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    #Make shure the topic belongs to the current user
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    return render(request, 'topic.txt', {'topic': topic, 'entries': entries})


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        #No data submitted, create a blank form
        form = TopicForm()
    else:
        #Post data submitted, process data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    return render(request, 'new_topic.txt', {'form': form})


@login_required
def new_entry(request, topic_id):
    """Add new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        #No data submitted, create a blank form
        form = EntryForm
    else:
        #Post data submitted, process data
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))
    return render(request, 'new_entry.txt', {'topic': topic, 'form': form})


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        #Initial request, prefill form with current entry
        form = EntryForm(instance=entry)
    else:
        #Post data submitted, process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))
    return render(request, 'edit_entry.txt', {'entry': entry,
                                              'topic': topic, 'form': form})
                                                
        

    
        
    
        
        
        
        
    
