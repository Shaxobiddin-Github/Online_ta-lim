from django.contrib import admin
from django.urls import path
from .views import (home_view, about_view, contact,add_video,course_detail,
                    cours_view, playlist_view, profile_view,update_teacher_profile,
                    teachers_profile_view, teacher_views,search_courses,
                    watch_video, user_login, register_user, playlist_view, teacher_details,
                     add_comment, delete_comment, edit_comment, toggle_like, update_profile, custom_logout)

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact, name='contact'),
    path('courses/', cours_view, name='courses'),
    path('playlist/<int:course_id>/', playlist_view, name='playlist'),
    path('profile/', profile_view, name='profile'),
    path('teacher_profile/', teachers_profile_view, name='teacher_profile'),
    path('teachers/', teacher_views, name='teachers'),
    path('watch/<int:video_id>/', watch_video, name='watch_video'),
    path('teachers/<int:teacher_id>/', teacher_details, name='teacher_details'),
    path('playlist/<int:course_id>/', playlist_view, name='playlist'),
    path('video/<int:video_id>/add_comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('toggle_like/<int:video_id>/', toggle_like, name='toggle_like'),
    path('update/', update_profile, name='update'),
    path('add_video/', add_video, name='add_video'),
    path('update_teachers/', update_teacher_profile, name='update_teachers'),
    path('search/', search_courses, name='search_courses'),  
    path('course/<int:pk>/', course_detail, name='course_detail'),
    
    
    path('login/', user_login, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', custom_logout, name='logout'),
    
]
