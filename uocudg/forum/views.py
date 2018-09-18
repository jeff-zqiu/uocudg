from django.shortcuts import render, get_object_or_404
from django.views import View as BaseView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from .form import *
from django.contrib.auth import views as auth_views
from warnings import warn


# TODO: implement password change/reset page


class View(BaseView):

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user
        else: return User.profile.defualt_user


class IndexView(View):
    template_name = "forum/index.html"

    def get(self, request):
        user = request.user
        self.index_post = Post.objects.order_by('-date')[:21]
        for this_post in self.index_post:
            this_post.comment_snaps = Comments.objects.filter(post=this_post)[:3]
        # if not user.is_authenticated:
        #     pass
        context = {
            'user':user,
            'latest_post_list': self.index_post,
        }
        return render(request, self.template_name, context)



class EditView(View):
    # parameter from LoginRequiredMixin to redirect to login page
    #login_url = '/forum/login/'

    form_class = PostForm
    template_name = 'forum/edit.html'
    action = '/forum/edit/'

    def get_post_data(self, post_id):
        if post_id:
            self.action = '/forum/' + str(post_id) + '/edit/'
            self.current_post = get_object_or_404(Post, pk=post_id)
            return {
            'title' : self.current_post.title,
            'content' : self.current_post.content,
        }
        else:
            return {'title':'', 'content':''}

    def get_post_title(self, request, data):
        if data['title']:
            title = data['title']
        elif data['display_name']:
            title = request.user.username
        else:
            title = Post.get_next_title()
        return title

    def get(self, request, post_id=0):
        initial = self.get_post_data(post_id)
        form = self.form_class(initial)
        return render(request, self.template_name,
                      {
                        'action' : self.action,
                        'form': form,
                        'post_id': post_id,
                      })

    def post(self, request, post_id=0):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if post_id:
                self.current_post = get_object_or_404(Post, pk=post_id)
                if data['title']: self.current_post.title=data['title']
                self.current_post.content = data['content']
                self.current_post.save()
            else:
                Post.objects.create(title=self.get_post_title(request, data),
                                    content=data['content'],
                                    author=self.get_user(request))
        return HttpResponseRedirect('/forum/')


def delete(request, post_id):
    if post_id:
        Post.objects.get(pk=post_id).delete()
    return HttpResponseRedirect('/forum/')

def clickup(request, post_id):
    def check_clicked(post_id, user):
        clicked_list = user.user.profile.clicked.split()
        if post_id in clicked_list:
            clicked_list.remove(post_id)
            user.clicked = ' '.join(clicked_list)
            user.save()
            return True
        else:
            clicked_list.append(post_id)
            user.clicked = ' '.join(clicked_list)
            user.save()
            return False

    this_post = Post.objects.get(pk=post_id)
    warn(type(request.user))
    if request.user.is_authenticated and not request.user.is_superuser:
        if check_clicked(post_id, request.user):
            this_post.clicks-=1
            this_post.save()
            return JsonResponse({'clicks' : this_post.clicks, 'clicked' : 'false'})
        this_post.clicks+=1
        this_post.save()
        return JsonResponse({'clicks' : this_post.clicks, 'clicked' : 'true'})

    else: return JsonResponse({'clicks' : this_post.clicks, 'clicked' : 'false'})



class ContentView(View):
    template_name = 'forum/content.html'

    def get(self, request, post_id=0):
        this_post = get_object_or_404(Post, pk=post_id)
        context = {
            'list_of_comments':Comments.objects.filter(post = this_post),
            'form': CommentForm(),
            'post': this_post,
        }
        return render(request, self.template_name, context)


class CommentView(View):
    template_name = 'forum/content.html'

    def post(self, request, post_id, comment_id=0):
        this_post = get_object_or_404(Post, pk=post_id)
        replay_to = None
        if comment_id:
            replay_to = get_object_or_404(Comments, pk=comment_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comments.objects.create(content=data['content'],
                                    parent_comment=replay_to,
                                    post=this_post,
                                    author=self.get_user(request),
                                    display_name=Comments.new_display_name(request, data))
        context = {
            'list_of_comments':Comments.objects.filter(post = this_post),
            'form': CommentForm(),
            'post': this_post,
        }
        return render(request, self.template_name, context)


class UserView(View):
    pass


class SignUpView(View):
    form_class = SignupForm
    template_name = 'forum/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.create_user(
                data['username'],
                data['email'],
                data['password']
            )
        return HttpResponseRedirect('/forum/')




class LoginView(auth_views.LoginView):
    pass



class LogoutView(auth_views.LogoutView):
    pass



