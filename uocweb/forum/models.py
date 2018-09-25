from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_image_file_extension



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_pk = models.IntegerField(default=0, editable=False)
    clicked = models.TextField(default='', null=True, blank=True)

    @classmethod
    def default_user(cls):
        try: anon = User.objects.get(pk=1)
        except ObjectDoesNotExist:
            anon = Profile.create_user('Anonymous', '', 'Anonymous').user
        return anon


    def is_anon(self):
        return self.user.pk == 1

    @classmethod
    def create_user(cls, username, email, password):
        user = User.objects.create_user(username, email, password)
        return cls.objects.create(user = user, user_pk = user.pk, clicked ='')

    def __str__(self):
        return self.user.username





class Post(models.Model):
    title = models.CharField(max_length=50, default='Untitled')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    content = models.TextField(default="Whoa such empty")
    clicks = models.IntegerField(default=0)
    tags = models.IntegerField(default=0)
    image = models.ImageField(upload_to='post/',
                              validators=[validate_image_file_extension],
                              null=True, blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_next_title(self):
        last_post = Post.objects.last()
        if last_post:
            return 'Secret #'+str(last_post.id+1)
        else: return 'Secret #1'





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
    def new_display_name(self, request, data):
        last_comment = Comments.objects.last()
        if last_comment:
            last_comment_id = last_comment.id
        else: last_comment_id = 0
        if request.user.is_authenticated:
            return '#' + str(last_comment_id + 1) + request.user.username
        else: return '#'+str(last_comment_id + 1) + ' '+ 'User'

    def __str__(self):
        name = self.display_name + ' : ' + str(self.content)[:30]
        if len(name) >= 29:
            name += '...'
        return name




