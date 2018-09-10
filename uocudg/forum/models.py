from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

defualt_user = User.objects.get(pk=2)


class Post(models.Model):
    title = models.CharField(max_length=50, default='Untitled')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    content = models.TextField(default="Whoa such empty")

    def __str__(self):
        return self.title

    @classmethod
    def get_next_title(self):
        return 'Secret #'+str(Post.objects.last().id+1)

class Comments(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField(default='')
    # if a post gets deleted, the comments will also be deleted (SQL CASCADE DELETE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # recursive model relationship
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name.username + ' : ' + str(self.content)[:20]


