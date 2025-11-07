"""
URL configuration for cloudmesh project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views 
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Includes Google OAuth routes
    path('', views.home, name="home"),
    path("", include("django_prometheus.urls")),
    path(views.service1.__name__, views.service1, name="service1"),
    path(views.service2.__name__, views.service2, name="service2"),
    path(views.service3.__name__, views.service3, name="service3"),
    path(views.service4.__name__, views.service4, name="service4"),
    path(views.service5.__name__, views.service5, name="service5"),
    path(views.service6.__name__, views.service6, name="service6"),
    path(views.service7.__name__, views.service7, name="service7"),
    path(views.service8.__name__, views.service8, name="service8"),
    path(views.register.__name__, views.register, name="register"),
    path('login/', views.loginpage, name="loginpage"),
    path('logout/', views.logoutuser, name="logout"),
    path('blogs/', views.blogs, name='blogs'),
    # path('lab/', views.lab, name='lab'),
    path('blogsfilter/<int:tag_id>', views.blogsfilter, name='blogsfilter'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path("alerts/", views.alerts_view, name="alert_list"),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('blog/<int:blog_id>/like/', views.add_like, name='add_like'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('reply/<int:reply_id>/delete/', views.DeleteReplyView.as_view(), name='delete_reply'),
    path('post/<int:post_id>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('blog/<int:post_id>/', views.post_detail, name='post_details'),


    #path('post/<int:post_id>/', views.blog_detail, name='post_detail'),


   


    # path('', views.contact_view, name='contact_view'),
    #path('contact/', views.contact_view, name='contact_view'),


    path('rest_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    path('rest_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_set.html"),name="password_reset_confirm"),
    path('rest_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
