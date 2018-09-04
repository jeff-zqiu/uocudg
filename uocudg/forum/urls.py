from django.urls import path, include
from . import views
from .views import IndexView, PostFormView, ContentView, CommentView


app_name = 'forum'
urlpatterns = [

    # /forum/
    path('', IndexView.as_view(), name = 'index'),

    # /forum/edit/
    path('edit/', PostFormView.as_view(), name = 'new'),
    path('<int:post_id>/edit/', PostFormView.as_view(), name='edit'),
    path('<int:post_id>/edit/delete/', views.delete, name='delete'),

    # /forum/<post_id>/
    path('<int:post_id>/', ContentView.as_view() , name='content'),

    # /forum/<post_id>/comment/
    path('<int:post_id>/comment/', CommentView.as_view(), name='new_comment'),
    path('<int:post_id>/comment/<int:comment_id>/', CommentView.as_view(), name='comment'),

    # # /forum/user/
    # path('user/<str:username>/', views.user, name='user'),
    # path('user/sign_up/', views.sign_up, name='sign_up'),
    # path('user/', include('django.contrib.auth.urls'))
]