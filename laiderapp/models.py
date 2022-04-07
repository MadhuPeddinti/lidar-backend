from django.db import models
# from django.contrib.postgres.fields import ArrayField
# Create your models here.
class creatingproject(models.Model):
    PROJECT_TITLE = models.CharField(max_length=255, blank=False, unique=True)
    DESCRIPTION = models.TextField(max_length=500, blank=True)
    IS_ACTIVE = models.BooleanField(blank=True, null=True)
    DATE = models.DateTimeField(auto_now=True)
    PROJECT_UPDATED_DATE = models.DateTimeField(blank=True, null=True)
    # FILEPATHS = ArrayField(models.TextField(default=''))

class las_files(models.Model):
    PROJECT = models.TextField(max_length=255, blank=False)
    TASK = models.TextField(max_length=100, blank=True)
    POTREE_HTML_FILE = models.TextField(max_length=255, blank=True)
    IS_ACTIVE = models.BooleanField(blank=True)
    IS_CONVERTED = models.BooleanField(blank=True)
    DATE = models.DateTimeField(auto_now=True)
    FILE = models.FileField(upload_to='media')
    TASK_UPDATED_DATE = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.TASK

