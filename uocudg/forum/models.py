from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=50, default='Untitled')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    content = models.TextField(default="Whoa such empty")
    clicks = models.IntegerField(default=0)
    tags = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @classmethod
    def get_next_title(self):
        return 'Secret #'+str(Post.objects.last().id+1)



class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, default='')
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField(default='')
    # if a post gets deleted, the comments will also be deleted (SQL CASCADE DELETE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # recursive model relationship
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    @classmethod
    def new_display_name(self):
        return '#'+str(Comments.objects.last().id+1)

    def __str__(self):
        return self.display_name + ' : ' + str(self.content)[:20]

class User(User):
    pass

