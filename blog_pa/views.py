from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.

def index(request):
	"""la página principal del Blog"""
	return render(request, 'blog_pa/index.html')
	
@login_required
def topics(request):
	"""Muestra todos los temas"""
	#topics = Topic.objects.order_by('date_added')
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	print (context)
	return render(request, 'blog_pa/topics.html', context)
	
@login_required
def topic(request, topic_id):
	"""Muestra un solo tema"""
	topic = Topic.objects.get(id=topic_id)
	check_topic_owner(request, topic)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	print (context)
	return render(request, 'blog_pa/topic.html', context)

@login_required
def new_topic(request):
	""" add a new topic"""
	if request.method != 'POST':
		form= TopicForm()
	else:
		form= TopicForm(data= request.POST)
		if form.is_valid():
			new_topic= form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			#form.save()
			return redirect('blog_pa:topics')
	context = {'form': form}
	return render(request, 'blog_pa/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Add a new entry"""
	topic = Topic.objects.get(id= topic_id)
	check_topic_owner(request, topic)
	if request.method != 'POST':
		form = EntryForm()
	else: 
		form = EntryForm(data= request.POST)
		if form.is_valid():
			#form.save()
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('blog_pa:topic', topic_id=topic_id)
	context = {'topic': topic, 'form': form}
	return render(request, 'blog_pa/new_entry.html', context)   

@login_required
def edit_entry(request, entry_id):
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	check_topic_owner(request, topic)
	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form= EntryForm(instance= entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('blog_pa:topic', topic_id=topic.id)
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'blog_pa/edit_entry.html', context)
	

def check_topic_owner(request, topic):
	"""Check if the topic owner maches the current user"""
	if topic.owner != request.user:
		raise Http404
	
