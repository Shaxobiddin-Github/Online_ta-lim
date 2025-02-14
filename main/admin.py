from django.contrib import admin
from .models import Comment,Video,SavedVideo,Course,Enrollment,Teacher,Student,Playlist,Like,Profile

# Register your models here.





admin.site.register(Video)

admin.site.register(SavedVideo)

admin.site.register(Course)

admin.site.register(Enrollment)

admin.site.register(Teacher)

admin.site.register(Student)

admin.site.register(Playlist)

admin.site.register(Like)

admin.site.register(Profile)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('student', 'video', 'commented_at', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('student__username', 'video__title', 'text')