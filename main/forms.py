
from django.contrib.auth.models import User
from django import forms
from .models import Comment, Course, Playlist
from .models import Video





class UpdateProfileForm(forms.ModelForm):
    old_pass = forms.CharField(widget=forms.PasswordInput(), required=True, label="Previous Password")
    new_pass = forms.CharField(widget=forms.PasswordInput(), required=False, label="New Password")
    c_pass = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirm Password")
    profile_picture = forms.ImageField(required=False, label="Update Pic")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        old_pass = cleaned_data.get("old_pass")
        new_pass = cleaned_data.get("new_pass")
        c_pass = cleaned_data.get("c_pass")

        if new_pass and new_pass != c_pass:
            raise forms.ValidationError("New passwords do not match!")

        return cleaned_data



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'box',
                'placeholder': 'Sharhingizni kiriting...',
                'rows': 5
            })
        }



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['playlist', 'title', 'video_file', 'cours', 'images']
        widgets = {
            'playlist': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video sarlavhasi'}),
            'video_file': forms.FileInput(attrs={'class': 'form-control'}),
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'playlist': 'Playlist tanlang',
            'title': 'Video nomi',
            'video_file': 'Video faylni yuklang',
            'cours': 'Kursni tanlang',
            'images': 'Videoga rasm yuklang',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Foydalanuvchi obyektini olish
        super(VideoForm, self).__init__(*args, **kwargs)
        
        if user:
            # Faqat foydalanuvchining o'ziga tegishli playlistlarni ko'rsatish
            self.fields['playlist'].queryset = Playlist.objects.filter(teacher=user.teacher_profile)
            
            # Faqat foydalanuvchining o'ziga tegishli kurslarni ko'rsatish
            self.fields['cours'].queryset = Course.objects.filter(teacher=user.teacher_profile)

from django import forms
from django.contrib.auth.models import User
from .models import Teacher




class TeacherProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Ism")
    last_name = forms.CharField(max_length=30, required=True, label="Familiya")

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'bio', 'expertise', 'profile_picture']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'O\'zingiz haqingizda ma\'lumot kiriting...'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mutaxassisligingizni kiriting (masalan, Python, Django)'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        # Agar user mavjud bo'lsa, uning first_name va last_name ni formaga yuklaymiz
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['first_name'].initial = kwargs['instance'].user.first_name
            self.fields['last_name'].initial = kwargs['instance'].user.last_name

    def save(self, commit=True):
        teacher = super(TeacherProfileForm, self).save(commit=False)
        # User modelining first_name va last_name maydonlarini yangilaymiz
        teacher.user.first_name = self.cleaned_data['first_name']
        teacher.user.last_name = self.cleaned_data['last_name']
        if commit:
            teacher.save()
            teacher.user.save()  # User modelini ham saqlaymiz
        return teacher