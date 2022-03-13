from django.db import models
from django.contrib.auth.models import User
from PIL import Image



class Profile(models.Model):
    # models.CASCADE -> mean is user is deleted than also delete the user profile, if we delete user than it wont delete the user profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
   

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,**kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 400:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
