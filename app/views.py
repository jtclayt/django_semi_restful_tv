from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from datetime import datetime

from app.models import Show


def index(request):
  return redirect(reverse('app:shows'))

def shows(request):
  context = {'shows': Show.objects.all()}
  return render(request, 'shows.html', context)

def view_show(request, show_id):
  try:
    context = {
      'show': Show.objects.get(id=show_id)
    }
  except Show.DoesNotExist:
    raise Http404('Show does not exist')
  return render(request, 'view_show.html', context)

def new_show(request):
  context = {
    'title': '',
    'network': '',
    'release_date': '',
    'description': ''
  }
  return render(request, 'new_edit_show.html', context)

def edit_show(request, show_id):
  try:
    show = Show.objects.get(id=show_id)
    context = {
      'title': show.title,
      'network': show.network,
      'release_date': show.release_date.strftime('%Y-%m-%d'),
      'description': show.description.strip(),
      'show_id': show.id
    }
  except Show.DoesNotExist:
    raise Http404('Show not found')
  return render(request, 'new_edit_show.html', context)


def create_show(request):
  if request.method == 'POST':
    request, title, network, desc, release_date = check_inputs(request)

    if not 'error-msg' in request.session:
      new_show = Show.objects.create(
        title=title,
        network=network,
        release_date=release_date,
        description=desc
      )
      return redirect(reverse('app:view_show', args=(new_show.id,)))
  return redirect(reverse('app:new_show'))

def update_show(request, show_id):
  if request.method == 'POST':
    request, title, network, desc, release_date = check_inputs(request)

    if not 'error-msg' in request.session:
      try:
        show = Show.objects.get(id=show_id)
        show.title = title
        show.network = network
        show.release_date = release_date
        show.description = desc
        show.save()
        return redirect(reverse('app:view_show', args=(show_id,)))
      except Show.DoesNotExist:
        raise Http404('Show not found')
  return redirect(reverse('app:edit_show'), args=(show_id,))

def destroy_show(request, show_id):
  try:
    Show.objects.get(id=show_id).delete()
  except Show.DoesNotExist:
    raise Http404('Show not found')
  return redirect('/')

def check_inputs(request):
  if 'error-msg' in request.session:
    del request.session['error-msg']
  title = request.POST['title']
  network = request.POST['network']
  desc = request.POST['desc']
  try:
    release_date = datetime.strptime(
      request.POST['release_date'], '%Y-%m-%d').date()
  except ValueError:
    request.session['error-msg'] = 'Release date must be a date'
  if len(title) < 2 or len(title) > 255:
    request.session['error-msg'] = 'Title must be between 2 and 255 characters'
  if len(network) < 2 or len(network) > 255:
    request.session['error-msg'] = 'Network must be between 2 and 255 characters'
  return (request, title, network, desc, release_date)
