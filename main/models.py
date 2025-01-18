from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from tinymce.models import HTMLField


class UserProfile(models.Model):

    image = models.ImageField(upload_to="images/avatars",null=True, blank=True)
    bio = HTMLField(blank=True,default="",max_length=3000)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)


    def __str__(self):

        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)



class PetCategory(models.Model):

    name = models.CharField(max_length=200,unique=True)
    donater = models.ForeignKey(User,related_name="user_categories",on_delete=models.CASCADE,null=True)
    slug = models.SlugField(null=True, blank=True)
    description =  HTMLField(blank=True,default="",max_length=3000)
    image = models.ImageField(upload_to="images/categories",null=True, blank=True)


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




@receiver(pre_save, sender=PetCategory)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)



class Pet(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    donater = models.ForeignKey(User,related_name="user_pets",on_delete=models.CASCADE,null=True)
    adopted = models.BooleanField(default=False)
    category = models.ForeignKey(PetCategory, related_name="pets", on_delete=models.CASCADE)
    description =  HTMLField(blank=True,default="",max_length=3000)
    image = models.ImageField(upload_to="images/pets",null=True, blank=True)


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
@receiver(pre_save, sender=Pet)
def store_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)



class ContactMessage(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    message = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):

        return f'{self.name}-{self.date}'


class ContactMessageAnswer(models.Model):

    message = models.ForeignKey(ContactMessage, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    reply = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f'{self.title}-{self.date}'
    


class Adoptation(models.Model):

    pet = models.OneToOneField(Pet, related_name='assigments' ,on_delete=models.CASCADE)
    adopter_list = models.ManyToManyField(User, related_name='adopters',blank=True)



    def __str__(self):

        return f'{self.pet}'



class  UserMessage(models.Model):

    receiver = models.ForeignKey(User, related_name="received" ,on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sended',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = HTMLField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    def __str__(self):

        return f'{self.sender}-{self.receiver}-{self.title}'



class ReplyUserMessage(models.Model):

    reply_message = models.ForeignKey(UserMessage,related_name="replies" ,on_delete=models.CASCADE)
    reply_receiver = models.ForeignKey(User, related_name="reply_received" ,on_delete=models.CASCADE)
    reply_sender = models.ForeignKey(User, related_name="reply_sended" ,on_delete=models.CASCADE)
    reply_title = models.CharField(max_length=200)
    reply_body = HTMLField(max_length=3000)
    reply_date = models.DateTimeField(auto_now_add=True)
   


    def __str__(self):

        return f'{self.reply_sender}-{self.reply_receiver}-{self.reply_title}'
    


