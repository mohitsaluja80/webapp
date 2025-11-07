from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField





# Create your models here.

class service(models.Model):
    service_name = models.CharField(max_length=100)
    service_icon = models.CharField(max_length=100,blank=True )
    service_url = models.CharField(max_length=50, blank=True)
    service_details = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.service_name

   
   
class service_categoreis(models.Model):
    name = models.ForeignKey(service, on_delete=models.CASCADE, related_name="service_url_name")
    category_title =  models.CharField(max_length=50)
    category_description = RichTextUploadingField(blank=True)
    category_icon = models.CharField(max_length=100)
   
class service_features(models.Model):
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=30)
    content = RichTextField(blank=True)

class address(models.Model):
    website_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    office_address = models.CharField(max_length=200, default="Offoce #123")

# class theam(models.Model):
#     theam = models.Choices("orange", "blue", "red", "green", "purpel")

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # comment = models.ForeignKey('self',on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Reply(models.Model):
    post = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class Features(models.Model):
    COLOR_CHOICES = (
    ('green','GREEN'),('pink','PINK'),('red','RED'),('blue','BLUE'),('purple', 'PURPLE'),('orange','ORANGE'))
    color_schem = models.CharField(choices=COLOR_CHOICES,max_length=12,default="blue")
    onfocus = models.BooleanField(default=False)
    testimonials = models.BooleanField(default=False)
    pricing = models.BooleanField(default=False)
    portfolio  = models.BooleanField(default=False)
    faq = models.BooleanField(default=False)
    team = models.BooleanField(default=False)
    recentblogs = models.BooleanField(default=False)
    services = models.BooleanField(default=False)
    about = models.BooleanField(default=False)
    contact = models.BooleanField(default=False)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email