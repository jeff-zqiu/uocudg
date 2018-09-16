from django.shortcuts import render, get_object_or_404
from django.views import View as BaseView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comments, User
from .form import PostForm, CommentForm, SignupForm, AuthenticatinoForm
from django.contrib.auth import views as auth_views
from warnings import warn


# TODO: implement password change/reset page
# todo: reload index post for every view causes performance issue


"""""
View Method Flow Chart:
    dispatch(): accepts a request argument plus arguments, and returns a HTTP response.
    http_method_not_allowed(): If the view was called with a HTTP method it doesn’t support, 
                                this method is called instead.
    (TemplateView) get_context_data(): Returns a dictionary representing the template context.
    (RedirectView) get_redirect_url(): Constructs the target URL for redirection.

    https://docs.djangoproject.com/en/2.1/ref/class-based-views/base/
"""""

class View(BaseView):

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user
        else: return User.defualt_user


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
                #todo: attribute error encountered when editing exisitng post
                if data['title']: self.current_post.title=data['title']
                self.current_post.content = data['content']
                self.current_post.save()
            else:
                Post.objects.create(title=self.get_post_title(request, data),
                                    content=data['content'],
                                    author=self.get_user(request))
        return HttpResponseRedirect('/forum/')


# function view because fuck it
def delete(request, post_id):
    if post_id:
        Post.objects.get(pk=post_id).delete()
    return HttpResponseRedirect('/forum/')


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
    def post(self, request, post_id, comment_id=0):
        comment_post = get_object_or_404(Post, pk=post_id)
        replay_to = None
        if comment_id:
            replay_to = get_object_or_404(Comments, pk=comment_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comments.objects.create(content=data['content'],
                                    parent_comment=replay_to,
                                    post=comment_post,
                                    author=self.get_user(request),
                                    display_name=Comments.new_display_name())

        return HttpResponseRedirect('/forum/' + str(post_id) + '/')


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
            User.objects.create_user(
                data['username'],
                data['email'],
                data['password']
            )
        return HttpResponseRedirect('/forum/')




class LoginView(auth_views.LoginView):
    pass



class LogoutView(auth_views.LogoutView):
    pass




# def user(request):
#     pass
#
# def user_login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return HttpResponseRedirect('/forum/')
#     else:
#         return HttpResponse('invalid login')
#
# def user_logout(request):
#     logout(request)
#     return HttpResponse("You're logged out.")
#
# def user_sign_up(request):
#     pass


