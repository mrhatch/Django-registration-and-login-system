import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
from users.images import resize


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    avatar_thumb_mini = models.ImageField(upload_to='profile_images', blank=True, null=True)
    avatar_thumb_small = models.ImageField(upload_to='profile_images', blank=True, null=True)
    avatar_thumb_medium = models.ImageField(upload_to='profile_images', blank=True, null=True)
    avatar_thumb_large = models.ImageField(upload_to='profile_images', blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    # def save(self, *args, **kwargs):
    #     super().save()
    #
    #     img = Image.open(self.avatar.path)
    #
    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)
    def save(self, *args, **kwargs):
        if not self.convert_avatar_images():
            raise Exception('Could not create thumbnail is it a valid file type?')
        super(Profile, self).save(*args, **kwargs)

    def convert_avatar_images(self):
        image = Image.open(self.avatar)
        # image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        thumb_name, thumb_extension = os.path.splitext(self.avatar.name)
        thumb_extension = '.jpg'
        thumb = BytesIO()

        large_thumb = image.crop_to_aspect(175, 175)
        large_thumb.thumbnail((175, 175), Image.ANTIALIAS)
        large_thumb_filename = '{}_avatar_thumb_large{}'.format(thumb_name, thumb_extension)
        large_thumb.save(thumb, 'JPEG')
        thumb.seek(0)
        self.avatar_thumb_large.save(large_thumb_filename, thumb, save=False)

        thumb = BytesIO()
        medium_thumb = image.crop_to_aspect(95, 95)
        medium_thumb.thumbnail((95, 95), Image.ANTIALIAS)
        medium_thumb_filename = '{}_avatar_thumb_medium{}'.format(thumb_name, thumb_extension)
        medium_thumb.save(thumb, 'JPEG')
        thumb.seek(0)
        self.avatar_thumb_medium.save(medium_thumb_filename, thumb, save=False)

        thumb = BytesIO()
        small_thumb = image.crop_to_aspect(40, 40)
        small_thumb.thumbnail((40, 40), Image.ANTIALIAS)
        small_thumb_filename = '{}_avatar_thumb_small{}'.format(thumb_name, thumb_extension)
        small_thumb.save(thumb, 'JPEG')
        thumb.seek(0)
        self.avatar_thumb_small.save(small_thumb_filename, thumb, save=False)

        thumb = BytesIO()
        mini_thumb = image.crop_to_aspect(32, 32)
        mini_thumb.thumbnail((32, 32), Image.ANTIALIAS)
        mini_thumb_filename = '{}_avatar_thumb_mini{}'.format(thumb_name, thumb_extension)
        mini_thumb.save(thumb, 'JPEG')
        thumb.seek(0)
        self.avatar_thumb_mini.save(mini_thumb_filename, thumb, save=False)

        return True
