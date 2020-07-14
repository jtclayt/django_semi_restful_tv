from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def index(request):
  return redirect(reverse('app:shows'))

def shows(request):
  return render(request, 'shows.html')

def new_show(request):
  return render(request, 'new_show.html')

def create_show(request):
  title = request.POST['title']
  network = request.POST['network']
  release_date = request.POST['release_date']
  desc = request.POST['desc']
  return redirect('/')