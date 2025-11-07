from django.contrib import admin
from .models import address, Post, Comment, Reply, service_categoreis, service_features, Features
from .models import service

# # Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display=('service_name', 'service_icon', 'service_details', 'service_url')



class ServiceDetailsDisplay(admin.ModelAdmin):
    model = service_categoreis
    list_display=( 'name', 'category_title','category_description')
   


class Address(admin.ModelAdmin):
    list_display=('website_name', 'email_id', 'phone')

class PostDisplay(admin.ModelAdmin):
    list_display=('title', 'content', 'date_posted')

class CommentDisplay(admin.ModelAdmin):
    list_display=('post', 'content', 'date_posted')

class ReplyDisplay(admin.ModelAdmin):
    list_display=('post', 'content', 'date_posted')

class FeatureDisply(admin.ModelAdmin):
    list_display = ('color_schem','faq',"team","portfolio",
                    "pricing","onfocus","testimonials","recentblogs", "services",
                    'about','contact')
    
class service_featuresDisplay(admin.ModelAdmin):
    list_display = ('title','icon','content')   

# class ArticleAdmin(admin.ModelAdmin):
#     ...
#     # your code here 
#     ...

#     class Media:
#         js = ('ckeditor.js',)
#         # do not write '/static/ckeditor.js' as Django automatically looks 
#         # in the static folder

admin.site.register(service, ServiceAdmin)
admin.site.register(address,Address)
admin.site.register(Post,PostDisplay)
admin.site.register(Comment,CommentDisplay)
admin.site.register(Reply,ReplyDisplay)
admin.site.register(service_categoreis,ServiceDetailsDisplay)
admin.site.register(Features,FeatureDisply)
admin.site.register(service_features,service_featuresDisplay)