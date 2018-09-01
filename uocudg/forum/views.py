from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comments
from .form import PostForm, CommentForm
from django.template import loader

from warnings import warn

def index(request):
    latest_post_list = Post.objects.order_by('-date')
    template = loader.get_template('forum/index.html')
    context = {
        'latest_post_list' : latest_post_list,
    }
    return HttpResponse(template.render(context, request))


def edit(request, post_id = 0):
    # if this is a POST request we need to process the form data
    current_data = {'title':'', 'content':''}
    warn(str(post_id))
    action = '/forum/edit/'
    if post_id:
        current_post = get_object_or_404(Post, pk=post_id)
        current_data = {
            'title' : current_post.title,
            'content' : current_post.content,
        }
        action = '/forum/'+str(post_id)+'/edit/'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if post_id:
                warn("updating form!")
                current_post.title=data['title']
                current_post.content = data['content']
                current_post.save()
            else:
                Post.objects.create(title=data['title'], content = data['content'], author='Test Author')
            return HttpResponseRedirect('/forum/')
    # if a GET (or any other method) we'll create a form
    else:
        form = PostForm(current_data)
    return render(request, "forum/edit.html", {'form':form, 'post_id' : post_id})


def delete(request, post_id):
    Post.objects.get(pk=post_id).delete()
    return HttpResponseRedirect('/forum/')


def content(request, post_id):
    this_post = get_object_or_404(Post, pk = post_id)
    form = CommentForm()
    list_of_comments = Comments.objects.filter(post = this_post)
    return render(request, 'forum/content.html', {'post':this_post,
                                                  'form': form,
                                                  'list_of_comments':list_of_comments})

def comment(request, post_id, comment_id = 0):
    # request will always be POST
    comment_post = get_object_or_404(Post, pk=post_id)
    replay_to = None
    if comment_id:
        replay_to = get_object_or_404(Comments, pk=comment_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        Comments.objects.create(name = data['name'], content = data['content'],
                                parent_comment = replay_to,
                                post = comment_post)
    return HttpResponseRedirect('/forum/'+str(post_id)+'/')


