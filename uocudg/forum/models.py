from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=50, default='Untitled')
    author = models.CharField(max_length=30, default='Visitor')
    date = models.DateTimeField(default = timezone.now)
    content = models.TextField(default="Whoa such empty")

    def __str__(self):
        return self.title

class Comments(models.Model):
    name = models.CharField(max_length=30, default='Visitor')
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField(default='')
    # if a post gets deleted, the comments will also be deleted (SQL CASCADE DELETE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # recursive model relationship
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name + ' : ' + str(self.content)

