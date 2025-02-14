
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from main.models import Student, Profile, Like,Teacher





@receiver(post_save, sender=User)
def add_student_if_not_teacher(sender, instance, created, **kwargs):
    if created:  # Foydalanuvchi yangi yaratilgan bo'lsa
        teacher_group = Group.objects.get(name='Teachers')
        if not instance.groups.filter(name='Teachers').exists():
            # Foydalanuvchi Teacher guruhiga kirgan bo'lmasa, Student modeliga qo'shamiz
            Student.objects.get_or_create(fio=instance)





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





@receiver(post_save, sender=Teacher)
def update_profile_on_teacher_update(sender, instance, created, **kwargs):
    """
    Teacher modeli yangilanganda Profile modelidagi profile_picture ni yangilash.
    """
    if not created:  # Faqat yangilash jarayonida ishlaydi (yangi yaratilgan bo'lsa emas)
        profile = instance.user.profile  # Teacher ga bog'langan user profilini olamiz
        if instance.profile_picture:  # Agar Teacher da profile_picture mavjud bo'lsa
            profile.profile_picture = instance.profile_picture  # Uni Profile ga o'tkazamiz
            profile.save()







@receiver(post_save, sender=Like)
def increment_video_likes(sender, instance, created, **kwargs):
    if created:
        instance.video.likes += 1
        instance.video.save()

@receiver(post_delete, sender=Like)
def decrement_video_likes(sender, instance, **kwargs):
    instance.video.likes -= 1
    instance.video.save()