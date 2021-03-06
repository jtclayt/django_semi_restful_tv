from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
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
        errors = Show.objects.basicValidator(request.POST)

        if len(errors) == 0:
            title = request.POST['title'].title()
            network = request.POST['network'].title()
            desc = request.POST['desc'].capitalize()
            release_date = datetime.strptime(
                request.POST['release_date'], '%Y-%m-%d').date()
            new_show = Show.objects.create(
                title=title,
                network=network,
                release_date=release_date,
                description=desc
            )
            return redirect(reverse('app:view_show', args=(new_show.id,)))

        for key, value in errors.items():
            messages.error(request, value)
    return redirect(reverse('app:new_show'))


def update_show(request, show_id):
    if request.method == 'POST':
        errors = Show.objects.basicValidator(request.POST, show_id)

        if len(errors) == 0:
            try:
                show = Show.objects.get(id=show_id)
            except Show.DoesNotExist:
                raise Http404('Show not found')
            show.title = request.POST['title'].title()
            show.network = request.POST['network'].title()
            show.description = request.POST['desc'].capitalize()
            show.release_date = datetime.strptime(
                request.POST['release_date'], '%Y-%m-%d').date()
            show.save()
            return redirect(reverse('app:view_show', args=(show_id,)))
        for key, value in errors.items():
            messages.error(request, value)
    return redirect(reverse('app:edit_show'), args=(show_id,))


def destroy_show(request, show_id):
    try:
        Show.objects.get(id=show_id).delete()
    except Show.DoesNotExist:
        raise Http404('Show not found')
    return redirect('/')
