from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [

    # /forum/
    path('', views.index, name = 'index'),

    # /forum/edit/
    path('edit/', views.edit, name = 'new'),
    path('<int:post_id>/edit/', views.edit, name='edit'),
    path('<int:post_id>/edit/delete/', views.delete, name='delete'),

    # /forum/<post_id>/
    path('<int:post_id>/', views.content, name='content'),

    # /forum/<post_id>/comment/
    path('<int:post_id>/comment/', views.comment, name='new_comment'),
    path('<int:post_id>/comment/<int:comment_id>/', views.comment, name='comment'),

]