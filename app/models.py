from django.db import models
from datetime import datetime


class ShowManager(models.Manager):
    def basicValidator(self, postData, show_id=False):
        errors = {}
        title = postData['title']
        network = postData['network']
        desc = postData['desc']
        try:
            release_date = datetime.strptime(
                postData['release_date'], '%Y-%m-%d').date()
        except ValueError:
            errors['date'] = 'Release date must be a date'
        if release_date > datetime.now().date():
            errors['date'] = 'Release date must be in the past'
        if len(title) < 2:
            errors['title'] = 'Title must be 2 or more characters'
        elif len(title) > 255:
            errors['title'] = 'Title must be 255 or less characters'
        elif len(Show.objects.filter(title=title)) > 0:
            is_same_title = Show.objects.get(id=show_id).title != title.title()
            if (not show_id) or is_same_title:
                errors['title'] = 'Title already in database'
        if len(network) < 2:
            errors['network'] = 'Network must be 2 or more characters'
        elif len(network) > 255:
            errors['network'] = 'Network must be 255 or less characters'
        if len(desc) == 0:
            errors['desc'] = 'Must provide a description'
        return errors


class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()
