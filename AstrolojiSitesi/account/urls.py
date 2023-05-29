from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from account.views import ChangePasswordView, daily_emails

urlpatterns = [
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("profile", views.update_user, name="profile"),
    path("logout", views.logout_request, name="logout"),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('send-daily-emails/', daily_emails, name='daily_emails'),
    path("reset_password", auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"), name="reset_password"),
    path("reset_password_sent", auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"), name="password_reset_done"),
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"), name="password_reset_complete"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"), name="password_reset_confirm"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path('new_topic/<board_id>', views.new_topic, name='new_topic'),
    path('all_topics', views.all_topics, name='all_topics'),
    path('topic_posts/<int:id>', views.topic_posts, name="topic_posts"),
    path('topic_posts/<int:id>/delete', views.delete_topic, name="topic_delete"),
    path('topic_posts/<int:id>/delete_post', views.delete_post, name="post_delete"),
    path('topic_posts/edit_post/<int:id>', views.edit_post, name="post_edit"),
    path('topic_posts/edit_topic/<int:id>', views.edit_topic, name="topic_edit"),
    path('post/<int:post_id>/reply/', views.post_reply, name='reply_post'),
    path('post/<int:post_id>/reply/<int:topic_id>', views.topic_posts),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('topic_posts/<int:topic_id>/like/', views.like_topic, name='like_topic'),
    path('topic_posts/<int:id>/delete2', views.delete_topic2, name="topic_delete2"),
    path('topic_posts/<int:id>/delete_post2', views.delete_post2, name="post_delete2"),



]
