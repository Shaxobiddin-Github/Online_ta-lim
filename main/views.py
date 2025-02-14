from datetime import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Video, Teacher, Profile, Student, SavedVideo, Enrollment,  Like,  Comment, Playlist
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from .forms import VideoForm, TeacherProfileForm




# Bosh sahifa ko‘rinishi

@login_required(login_url='/login')
def home_view(request):
    total_likes = Like.objects.count()
    # total_like=Like.video.likes.count()
    total_comments = Comment.objects.count()
    total_playlists = Playlist.objects.count()
    # Kurslar va ular haqidagi ma'lumotlarni olish
    all_courses = Course.objects.all()
    start_course = all_courses.order_by('-created_at')
    is_teacher = request.user.groups.filter(name='Teachers').exists()
    profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
    course_html = Course.objects.filter(id=1).first()
    course_css = Course.objects.filter(id=2).first()
    course_java = Course.objects.filter(id=3).first()
    course_py = Course.objects.filter(id=4).first()


        

    context = {
        'all_courses': all_courses,
        'start_course': start_course,
        'is_teacher': is_teacher,  # Teacherni aniq qilish
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_playlists': total_playlists,
        'profile': profile,  # User asosida profile topamiz
        # 'total_like':total_like
        'course_html': course_html,  
        'course_css': course_css,  
        'course_java': course_java,
        'course_py': course_py,
    }
    return render(request, 'home.html', context)


# Biz haqimizda sahifasi
@login_required(login_url='/login')
def about_view(request):
        # Kurslar sonini hisoblash
    total_courses = Course.objects.count()
    # O'qituvchilar sonini hisoblash
    total_teachers = Teacher.objects.count()
    # Talabalar sonini hisoblash
    total_students = Student.objects.count()
    profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
    is_teacher = request.user.groups.filter(name='Teachers').exists()
    context = {
        'is_teacher': is_teacher,  # Teacherni aniq qilish
        'profile': profile,  # User asosida profile topamiz
        'total_courses': total_courses,
        'total_teachers': total_teachers,
        'total_students': total_students,  # Talabalar sonini hisoblash
    }
    return render(request, 'about.html', context)


# def contact_view(request):
#     profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
#     is_teacher = request.user.groups.filter(name='Teachers').exists()
#     context = {
#         'is_teacher': is_teacher,  # Teacherni aniq qilish
#         'profile': profile,  # User asosida profile topamiz
#     }
#     return render(request, 'contact.html', context)


# Kurslar sahifasi
@login_required(login_url='/login')
def cours_view(request):
    # Barcha kurslarni olish
    all_courses = Course.objects.all()
    start_course = all_courses.order_by('-created_at')
    profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
    is_teacher = request.user.groups.filter(name='Teachers').exists()

    context = {
        'all_courses': all_courses,
        'start_course': start_course,
        'is_teacher': is_teacher,  # Teacherni aniq qilish
        'profile': profile,  # User asosida profile topamiz
    }
    return render(request, 'courses.html', context)


# Kursning barcha videolarini ko‘rish uchun oynasi
@login_required(login_url='/login')
def playlist_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    video_count = videos.count()
    is_teacher = request.user.groups.filter(name='Teachers').exists()

    context = {
        'course': course,
        'videos': videos,
        'video_count': video_count,
        'is_teacher': is_teacher,
    }
    return render(request, 'playlist.html', context)

    



def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Video uchun barcha like'larni olish
    likes_count = Like.objects.filter(video=video).count()

    # Foydalanuvchi shu video uchun like qilganmi?
    if hasattr(request.user, 'students'):
        is_liked = Like.objects.filter(student=request.user.students, video=video).exists()
    elif request.user.groups.filter(name='Teachers').exists():
        # Agar foydalanuvchi Teacher bo'lsa, Like qilganmi yoki yo'qligini tekshirish
        is_liked = False  # Agar Teacher uchun Like modeli mavjud bo'lmasa, bu qatorni o'zgartiring
    else:
        is_liked = False


    context = {
        'video': video,
        'course_id': video.cours.id,
        'likes_count': likes_count,  # Like sonini yuborish
        'is_liked': is_liked,  # Foydalanuvchi like qilganini ko'rsatish
    }

    return render(request, 'watch_video.html', context)


# Profil sahifasi
@login_required(login_url='login')
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
    is_teacher = request.user.groups.filter(name='Teachers').exists()
    student = Student.objects.get(fio=request.user)
    

    return render(request, 'profile.html', {'profile': profile, 'is_teacher': is_teacher, 'student': student})







# O‘qituvchilar uchun profil sahifasi
@login_required(login_url='login')
def teachers_profile_view(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
    is_teacher = request.user.groups.filter(name='Teachers').exists()
    
    context = {
        'teacher': teacher,
        'profile': profile,
        'is_teacher': is_teacher,  # Teacherni aniq qilish
        'is_own_profile':True,
        'total_comments': teacher.total_comments
    }
    return render(request, 'teacher_profile.html', context)

# @login_required(login_url='login')
def teacher_details(request, teacher_id):
    """
    Barcha foydalanuvchilar istalgan teacher profilini ko‘ra oladi.
    Agar teacher o‘z profiliga kirsa, bu narsa aniq belgilanadi.
    """
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    profile = get_object_or_404(Profile, user=teacher.user)
    is_teacher = request.user.groups.filter(name='Teachers').exists()
    is_own_profile = teacher.user == request.user  # Agar teacher o‘z profiliga kirsachi?
    videos = teacher.videos.all()

    context = {
        'teacher': teacher,
        'profile': profile,
        'is_teacher': is_teacher,
        'is_own_profile': is_own_profile,
        'videos': videos,  # Teacherga tegishli videolar olish
    }
    return render(request, 'teacher_profile.html', context)

# O‘qituvchilar ro‘yxati sahifasi
@login_required(login_url='/login')
def teacher_views(request):

    all_teachers = Teacher.objects.all()
    profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
    is_teacher = request.user.groups.filter(name='Teachers').exists()


    context = {
        'all_teachers': all_teachers,
        'is_teacher': is_teacher,  
        'profile': profile,  
    }
    return render(request, 'teachers.html', context)


# Yangilash sahifasi
class UpdateView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
        is_teacher = request.user.groups.filter(name='Teachers').exists()

        context = {
            'is_teacher': is_teacher,  # Teacherni aniq qilish
            'profile': profile,  # User asosida profile topamiz
        }

        return render(request, 'update.html', context)




def user_login(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)  # User asosida profile topamiz
        is_teacher = request.user.groups.filter(name='Teachers').exists()
    else:
        # Agar foydalanuvchi tizimga kirgan bo'lmasa, login sahifasini ko'rsatish
        profile = None
        is_teacher = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, 'Invalid username or password!')

    context = {
        'is_teacher': is_teacher,  # Teacherni aniq qilish
        'profile': profile,  # User asosida profile topamiz
    }
    return render(request, 'login.html', context)





# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('home')  # Logoutdan keyin home sahifasiga yo'naltirish


def register_user(request):
    is_teacher = request.user.groups.filter(name='Teachers').exists()

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture')

        # 🔴 Parollar bir-biriga mosligini tekshiramiz
        if password1 != password2:
            return render(request, 'register.html', {'error': "Passwords do not match!"})

        # 🔴 Foydalanuvchi mavjudligini tekshiramiz
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Username already taken!"})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': "Email already in use!"})

        # 🟢 Yangi user yaratamiz
        user = User.objects.create_user(username=username, email=email, password=password1)

        # 🟢 Profilni yaratish yoki yangilash
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            profile.profile_picture = profile_picture
            profile.save()

        # 🔵 Userni tizimga kiritamiz (login)
        login(request, user)
        return redirect('home')  # Bosh sahifaga yo‘naltiramiz

    context = {
        'is_teacher': is_teacher,  # Teacherni aniq qilish
    }

    return render(request, 'register.html', context)









# Kurslarni ro'yxatini ko'rsatish uchun view
def courses_view(request):
    # Kurslarni olish
    start_course = Course.objects.all()
    return render(request, 'courses.html', {'start_course': start_course})

# Playlist ma'lumotlarini ko'rsatish uchun view
def playlist_view(request, course_id):
    # Kursni id orqali olish
    course = get_object_or_404(Course, id=course_id)

    # Videolarni olish (course modelidagi related_name orqali)
    videos = course.videos.all()

    # Teacher haqida ma'lumot olish
    teacher = course.teacher

    return render(request, 'playlist.html', {'course': course, 'videos': videos, 'teacher': teacher})







# ------------------------------------add Comment --------------------------------




def add_comment(request, video_id):
    video = Video.objects.get(id=video_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_box')
        # Yangi comment yaratish
        comment = Comment(student=request.user, video=video, text=comment_text)
        comment.save()  # Kommentni saqlash
        return redirect('watch_video', video_id=video.id)  # Kommentdan so'ng video sahifasiga qaytish
    return render(request, 'watch_video.html', {'video': video})

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        new_text = request.POST.get('comment_box')

        if new_text:
            comment.text = new_text
            comment.edited_at = timezone.now()  # Tahrir qilingan vaqtni yangilash
            comment.save()

            # Tahrir qilingan kommentni ko'rsatish uchun video sahifasiga qaytarish
            return redirect('watch_video', video_id=comment.video.id)
        else:
            # Agar yangi matn bo'lmasa, xatolik xabarini ko'rsatish
            return render(request, 'edit_comment.html', {
                'comment': comment,
                'error': 'Comment text cannot be empty!'
            })

    return render(request, 'edit_comment.html', {'comment': comment})



def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.student != request.user:
        raise Http404("You are not allowed to delete this comment.")
    
    video_id = comment.video.id
    comment.delete()  # Kommentni o'chirish
    return redirect('watch_video', video_id=video_id)  # O'chirishdan so'ng video sahifasiga qaytish





def toggle_like(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    student = request.user.students  # Foydalanuvchining 'Student' modeliga murojaat qilish
    
    # Agar like bor bo'lsa, uni olib tashlash, aks holda yangi like yaratish
    like, created = Like.objects.get_or_create(student=student, video=video)
    if not created:  # Agar like bor bo'lsa, uni olib tashlash
        like.delete()
        return JsonResponse({'liked': False})  # Like o'chirilganligini bildirish
    return JsonResponse({'liked': True})  # Like qo'shilganligini bildirish











def update_profile(request):
    if request.method == 'POST':
        # Foydalanuvchi ma'lumotlarini olish
        new_username = request.POST.get('name')
        new_email = request.POST.get('email')
        old_password = request.POST.get('old_pass')
        new_password = request.POST.get('new_pass')
        confirm_password = request.POST.get('c_pass')
        profile_picture = request.FILES.get('picture')  # Rasmni olish

        user = request.user  # Joriy foydalanuvchi

        # Username va emailni yangilash
        if new_username and new_username != user.username:
            user.username = new_username
        if new_email and new_email != user.email:
            user.email = new_email

        # Parolni tekshirish va yangilash
        if old_password and new_password and confirm_password:
            if not user.check_password(old_password):
                messages.error(request, "Eski parol noto'g'ri!")
                return redirect('update')
            if new_password != confirm_password:
                messages.error(request, "Yangi parollar mos kelmaydi!")
                return redirect('update')
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Seansni yangilash
            messages.success(request, "Parolingiz muvaffaqiyatli yangilandi!")

        # Profil rasmini yangilash
        profile, created = Profile.objects.get_or_create(user=user)
        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        # Foydalanuvchi ma'lumotlarini saqlash
        user.save()

        messages.success(request, "Profil muvaffaqiyatli yangilandi!")
        return redirect('profile')  # Yoki boshqa bir sahifaga yo'naltiring

    return render(request, 'update.html')








# views.py
@login_required(login_url='login/')
def contact(request):
    is_teacher = request.user.groups.filter(name='Teachers').exists()
    if request.method == 'POST':
        # Formadan ma'lumotlarni olish
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('msg')

        # Xabar matnini tayyorlash
        subject = f"Yangi xabar: {name}"
        body = f"Ism: {name}\nEmail: {email}\nTelefon raqam: {number}\n\nXabar:\n{message}"

        try:
            # Email yuborish
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,  # Kimdan (admin email)
                [settings.EMAIL_HOST_USER],  # Kimga (admin email)
                fail_silently=False,
            )
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi!")
            return redirect('contact')  # Contact sahifasiga qaytish
        except Exception as e:
            messages.error(request, "Xabar yuborishda xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")
            return redirect('contact')

    return render(request, 'contact.html', {'is_teacher':is_teacher})






@login_required
def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, user=request.user)  # user parametrini uzatish
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user.teacher_profile  # Foydalanuvchi Teacher modeliga bog'langan deb faraz qilamiz
            video.save()
            return redirect('home')  # Video qo'shilgandan keyin yo'naltirish
    else:
        form = VideoForm(user=request.user)  # GET so'rovda ham user parametrini uzatish
    
    return render(request, 'add_video.html', {'form': form})


@login_required
def update_teacher_profile(request):
    # Tizimga kirgan foydalanuvchining Teacher profilini topamiz
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_profile')  # Yangilangan ma'lumotlarni ko'rish uchun yo'naltirish
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, 'update_teachers.html', {'form': form})




def search_courses(request):
    query = request.GET.get('search_box', '')  # Search so'rovini olamiz
    results = []

    if query:
        # Kurs nomi yoki tavsifida qidiruv
        results = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query)

    return render(request, 'search_results.html', {'results': results, 'query': query})




def course_detail(request, pk):
    # Kursni ID bo'yicha topamiz
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'playlist.html', {'course': course})