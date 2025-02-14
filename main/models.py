from django.db import models
from django.contrib.auth.models import User

# ---------------------------------------------Teachers --------------------------------

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(null=True, blank=True)  # O‘qituvchi haqida qisqa ma’lumot
    expertise = models.CharField(max_length=200, null=True, blank=True)  # Mutaxassislik (masalan, Python, Django)
    profile_picture = models.ImageField(upload_to='teachers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_playlists(self):
        return self.playlists.count()  # Bog'langan playlistlar soni

    @property
    def total_videos(self):
        return Video.objects.filter(playlist__teacher=self).count()  # Bog'langan videolar soni

    @property
    def total_likes(self):
        return Video.objects.filter(playlist__teacher=self).aggregate(models.Sum('likes')).get('likes__sum', 0) or 0


    @property
    def total_comments(self):
        from django.db.models import Count
        return Comment.objects.filter(video__author=self).count() 

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    

class Playlist(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.title



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to='courses/', null=True, blank=True)  # Kursdan ko'raq rasm


    @property
    def video_count(self):
        return self.videos.count() 

    def __str__(self):
        return self.title




class Video(models.Model):
    playlist = models.ForeignKey(
        'Playlist', on_delete=models.CASCADE, related_name='videos', null=True, blank=True)  
    author = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='videos') 
    title = models.CharField(max_length=200) 
    likes = models.PositiveIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)  
    cours = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='videos', blank=True, null=True
    )  # Kursga bog'langan video
    images = models.ImageField(upload_to='video_images/', null=True, blank=True)  # Videoning rasmi

    def __str__(self):
        return self.title
    













# ----------------------------------------------------------------O'quvchi------------------------------------------

class Student(models.Model):
    fio = models.OneToOneField(User, on_delete=models.CASCADE, related_name='students')
    profile_picture = models.ImageField(upload_to='students/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)  # Qisqacha ma'lumot
    enrolled_courses = models.ManyToManyField(Course, through='Enrollment', related_name='students')

    def total_completed_lessons(self):
        return self.enrollments.filter(is_completed=True).count()

    

    @property
    def total_liked_videos(self):
        return self.likes.count()

    @property
    def total_saved_videos(self):
        return self.saved_videos.count()

    @property
    def total_comments(self):
        return self.fio.comments.count()

    
    def __str__(self):
        return self.fio.first_name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    progress = models.PositiveIntegerField(default=0)  # Kurs tugallanish foizi
    is_completed = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.fio.first_name} - {self.course.title}"

    


class Like(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='liked_by')
    liked_at = models.IntegerField(default=0)
    class Meta:
        unique_together = ('student', 'video')  # Bir o‘quvchi bir videoga faqat bir marta layk bosishi mumkin

    def __str__(self):
        return f"{self.student.fio.first_name} liked {self.video.title}"


class SavedVideo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='saved_videos')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'video')  # Bir o‘quvchi bir videoni faqat bir marta saqlashi mumkin

    def __str__(self):
        return f"{self.student.fio.first_name} saved {self.video.title}"


class Comment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # Foydalanuvchi modelidan foydalanish
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')  # Video modeli bilan bog'lanadi
    text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)  # Komment tahrirlanganda vaqt qo'shish
    is_approved = models.BooleanField(default=True)  # Kommentni tasdiqlash flag'i

    def __str__(self):
        return f"{self.student.username} commented on {self.video.title}"
    
    # -------------------------------------------------------END O'quvchi----------------------------------------


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Userga bog'lanish
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Rasm maydoni

    def __str__(self):
        return self.user.username