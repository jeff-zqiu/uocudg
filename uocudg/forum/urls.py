from django.urls import path, include
from . import views

app_name = 'forum'
urlpatterns = [

    # /forum/
    path('', views.IndexView.as_view(), name = 'index'),

    # /forum/edit/
    path('edit/', views.EditView.as_view(), name = 'new'),
    path('<int:post_id>/edit/', views.EditView.as_view(), name='edit'),
    path('<int:post_id>/edit/delete/', views.delete, name='delete'),

    # /forum/<post_id>/
    path('<int:post_id>/', views.ContentView.as_view() , name='content'),
    path('<int:post_id>/clickup/', views.ClickUpView.as_view(), name='clickup'),

    # /forum/<post_id>/comment/
    path('<int:post_id>/comment/', views.CommentView.as_view(), name='new_comment'),
    path('<int:post_id>/comment/<int:comment_id>/', views.CommentView.as_view(), name='comment'),

    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(template_name='forum/login.html',
                                           extra_context = {'next': '/forum/'}), name='login'),
    path('logout/', views.LogoutView.as_view(), name = 'logout'),

    # /forum/user/
    path('user/<str:username>/', views.UserView.as_view(), name='user'),
]