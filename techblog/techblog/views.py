from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from web.models import service, Post, Comment, Reply, Like, service_categoreis, Features, service_features
from web.models import address, NewsletterSubscriber
from django.contrib.auth.forms import UserCreationForm 
from .form import createuserForm, CommentForm, ContactForm, NewsletterSubscriptionForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic import ListView, DetailView
from .form import CommentForm, ReplyForm, PostForm
from taggit.models import TaggedItem
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import json
import ssl
import re

INVALID_SSL_CONTEXT = ssl._create_unverified_context

import requests
import os
from django.shortcuts import render

# Vector DB service URL
VECTOR_DB_URL = os.getenv("VECTOR_DB_URL")
#from langchain_openai import ChatOpenAI
#from langchain.schema import SystemMessage, HumanMessage

# Load environment variables
VECTOR_DB_URL = os.getenv("VECTOR_DB_URL")
#llm = ChatOpenAI(model_name="gpt-4", temperature=0)
import json
import requests


import requests
import json


import re
import json

import re
import json



import json
import requests


# def fetch_latest_alert():
#     """Fetch the latest alert from the Vector DB and extract relevant details."""
#     if not VECTOR_DB_URL:
#         print("❌ VECTOR_DB_URL is not set.")
#         return None

#     print(f"🔍 Fetching alerts from: {VECTOR_DB_URL}")

#     try:
#         response = requests.get(f'{VECTOR_DB_URL}/search-alerts/')
#         response.raise_for_status()
        
#         data = response.json()
      
#         #print("✅ API Response:", json.dumps(data, indent=2))  # Log full response

#         if not data.get("alerts") or not data["alerts"].get("documents") or len(data["alerts"]["documents"]) == 0:
#             print("⚠ No alerts found in response.")
#             return None

#         # Extract and parse the latest alert
#         latest_alert_entry = data["alerts"]["documents"][0]  # First alert document

#         if not latest_alert_entry:
#             print("⚠ Alert content is empty.")
#             return None

#         # Clean and parse the alert content
#         for alert in data['alerts']['metadatas']:
#             alert_list = []
#             for alert_data in alert:
    
#                 useful_data = {
#                     "receiver": alert_data.get("receiver"),
#                     "status": alert_data.get("status"),
#                     "alerts": alert_data.get("alerts"),
#                     "groupLabels_alertname": alert_data.get("groupLabels_alertname"),
#                     "groupLabels_namespace": alert_data.get("groupLabels_namespace"),
#                     "commonLabels_alertname": alert_data.get("commonLabels_alertname"),
#                     "commonLabels_namespace": alert_data.get("commonLabels_namespace"),
#                     "commonLabels_pod": alert_data.get("commonLabels_pod"),
#                     "commonLabels_severity": alert_data.get("commonLabels_severity"),
#                     "commonAnnotations_summary": alert_data.get("commonAnnotations_summary"),
#                     "commonAnnotations_description": alert_data.get("commonAnnotations_description"),
#                     "externalURL": alert_data.get("externalURL"),
#                     "version": alert_data.get("version"),
#                     "groupKey": alert_data.get("groupKey"),
#                     "logs": alert_data.get("logs"),
#                     "events": alert_data.get("events"),
#                     "solution": alert_data.get("soluton"),
#                 }

#                 print("✅ Parsed Useful Data:", json.dumps(useful_data, indent=2))
#                 alert_list.append(useful_data)
#         return alert_list

#     except requests.RequestException as e:
#         print(f"❌ Request failed: {e}")
#         return None
# def troubleshoot_alert(alert_text):
#     """Get AI troubleshooting suggestions based on the alert text."""
#     if not alert_text:
#         return "No alerts found."

#     messages = [
#         SystemMessage(content="You are an expert SRE. Use alerts to debug issues."),
#         HumanMessage(content=f"Troubleshoot this issue based on this alert:\n{alert_text}")
#     ]

#     response = llm(messages)
#     return response.content

# def alert_dashboard(request):
#     """Django view to fetch the latest alert and AI troubleshooting suggestion."""
#     latest_alert = fetch_latest_alert()
#     ai_suggestion = troubleshoot_alert(latest_alert) if latest_alert else "No alerts found."

#     print(f"🚀 Sending to Template -> Latest Alert: {latest_alert}")  # Debugging
#     print(f"🚀 Sending to Template -> AI Suggestion: {ai_suggestion}")  # Debugging

#     return render(request, "alert_dashboard.html", {
#         "latest_alert": latest_alert,
#         "ai_suggestion": ai_suggestion
#     })

# def get_ai_suggestion(alert_text):
#     """Generate an AI-based troubleshooting suggestion."""
#     if not alert_text:
#         return "No alerts found."

#     messages = [
#         SystemMessage(content="You are an expert SRE. Use alerts to debug issues."),
#         HumanMessage(content=f"Troubleshoot this issue based on this alert:\n{alert_text}")
#     ]

#     response = llm(messages)

#     print(f"🤖 AI Suggestion: {response.content}")  # Debugging
#     return response.content

# def alerts_view(request):
#     """Django view to display alerts and AI troubleshooting suggestions."""
#     latest_alert = fetch_latest_alert()
#     #ai_suggestion = get_ai_suggestion(latest_alert)


#     print(f"📢 Latest Alert: {latest_alert}")  # Debugging
#     #print(f"🤖 AI Suggestion: {ai_suggestion}")  # Debugging

#     return render(request, "alerts.html", {"alert": latest_alert})

def tagdata():
    mylist = []
    mydict = {}
    for item in TaggedItem.objects.all():
        mylist.append(item.tag.name)
    for i in mylist:
        mydict[i] = mylist.count(i)
    return mydict



def home(request):
    color_scheme =  Features.objects.get().color_schem
    serviceData = service.objects.all()
    addressData = address.objects.all()
    featureData = service_features.objects.all()
    is_onfocus_enabled = Features.objects.filter(onfocus=True)
    is_testimonials_enabled  =  Features.objects.filter(testimonials=True)
    is_pricing_enabled  =  Features.objects.filter(pricing=True)
    is_faq_enabled  =  Features.objects.filter(faq=True)
    is_portfolio_enabled  =  Features.objects.filter(portfolio=True)
    is_recentblogs_enabled = Features.objects.filter(recentblogs=True)
    is_team_enabled = Features.objects.filter(team=True)
    is_services_enabled = Features.objects.filter(services=True)
    is_about_enabled = Features.objects.filter(about=True)
    is_contact_enabled = Features.objects.filter(contact=True)
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']
            subject = f'Contact Us Form Submission from {name}'
            message_body = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
            from_email = email
            recipient_list = ['mohitsaluja@gmail.com']
            try:
                send_mail(subject, message_body, from_email, recipient_list)
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        contact_form = ContactForm()
    data = {'serviceData': serviceData, 'addressData': addressData,
            "featureData":featureData,
            "onfocus":is_onfocus_enabled,"testimonials": is_testimonials_enabled,
            "pricing":is_pricing_enabled,
            "portfolio":is_portfolio_enabled,
            "faq":is_faq_enabled,
            "recentblogs":is_recentblogs_enabled,
            "team": is_team_enabled,
            "services": is_services_enabled,
            "color_scheme":color_scheme,
            "about":is_about_enabled,
            "contact":is_contact_enabled,
            "contact_form": contact_form,
            }
    

            
    return render(request, "index.html", data)


def reset_password(request):
    form = auth_views.PasswordResetView.as_view()
    print()
    context = {"form": form}
    return render(request, 'password_reset.html', context)


import requests

from django.conf import settings 
from django.http import JsonResponse

from .prom import PrometheusClient  # Import the service class

def prometheus_metrics_view():
    prometheus = PrometheusClient()
    metrics = prometheus.get_cluster_metrics()
    return metrics


JENKINS_BASE_URL = settings.JENKINS_BASE_URL # Replace with your ArgoCD URL
ARGO_BASE_URL = settings.ARGO_BASE_URL
JENKINS_API_TOKEN = settings.JENKINS_TOKEN
JENKINS_USER = settings.JENKINS_USER
ARGOCD_USERNAME = settings.ARGO_USER
ARGOCD_PASSWORD = settings.ARGO_PASSWORD
JENKINS_PIPELINE=settings.JENKINS_PIPELINE

# def get_argocd_token():
#     """Authenticate with ArgoCD and get a session token."""
#     url = f"{ARGO_BASE_URL}/api/v1/session"
#     payload = {"username": ARGOCD_USERNAME, "password": ARGOCD_PASSWORD}

#     try:
#         response = requests.post(url, json=payload, timeout=10, verify=False)
#         response.raise_for_status()
#         return response.json().get("token")  # Extract token from response
#     except requests.exceptions.RequestException as e:
#         return None

# def get_argocd_applications():
#     """Fetch application data from ArgoCD API using session authentication."""
#     token = get_argocd_token()
#     if not token:
#         return JsonResponse({"error": "Failed to authenticate with ArgoCD"}, status=401)

#     url = f"{ARGO_BASE_URL}/api/v1/applications"
#     headers = {"Authorization": f"Bearer {token}"}

#     try:
#         response = requests.get(url, headers=headers, timeout=10, verify=False)
#         #response.raise_for_status()
#         print(response.status_code)
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({"error": str(e)}, status=500)




# def fetch_jenkins_data(api):

#     if api == "ci":
#         url = f"{JENKINS_BASE_URL}/job/{JENKINS_PIPELINE}/api/json"
#     if api == "jobs":
#         url = f"{JENKINS_BASE_URL}/api/json"
    
#     response = requests.get(url, auth=(JENKINS_USER, JENKINS_API_TOKEN))
    
#     if response.status_code == 200:
#        return response.json()
#     else:
#         return {"error": "Failed to fetch Jenkins data"}
    

# @login_required(login_url='loginpage')
# def lab(request):
#     prom_data = prometheus_metrics_view()
#     addressData = address.objects.all()
#     color_scheme =  Features.objects.get().color_schem
#     argo_data = {}
#     jenkins_data = {}
#     if "metadata" in get_argocd_applications():
#         argo_service = "🟢"
#         argo_data.update(get_argocd_applications())
#     else:
#         argo_service = "🔴"
#         argo_data = ""
    
#     if "jobs" in fetch_jenkins_data("jobs"):
#         jenkins_service = "🟢"
#         jenkins_data.update(fetch_jenkins_data("ci"))

#         color_mapping = {
#             "blue": "✅", 
#             "red": "❌",
#             "yellow": "⚠️",
#             "grey": "⚪",   
#             "disabled": "🚫",
#             "aborted": "⏹️",
#             "blue_anime": '<div class="spinner"></div>',
#             "red_anime": '<div class="spinner"></div>',
#             "yellow_anime": '<div class="spinner"></div>',
#             "grey_anime": '<div class="spinner"></div>'
#         }

#         jenkins_status = color_mapping.get(jenkins_data.get("color"), "❓")  # Default to ❓ if unknown

#     else:
#             jenkins_service = "🔴"
#             jenkins_data = "" 
#             jenkins_status = "❓"  # Unknown state
            
#     data = {'addressData': addressData, 
#             "color_scheme": color_scheme,
#             "Jenkins_service": jenkins_service,
#             "argo_service" : argo_service,
#             "jenkins_data": jenkins_data,
#             "jenkins_build_status": jenkins_status,
#             "argo_data" : argo_data,
#             "prom": prom_data
#             }
            
#     return render(request, "lab.html", data)
  
  



def register(request):
    form = createuserForm()
    if request.method == 'POST':
        form = createuserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email confirmation
            user.save()

            # Generate email verification token
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            verification_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            verification_url = f"http://{current_site.domain}{verification_link}"

            # Send verification email
            subject = "Activate Your Account"
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'verification_url': verification_url,
            })
            email = EmailMessage(subject, message, to=[user.email])
            email.send()

            messages.success(request, f"Verification email sent to {user.email}. Please check your inbox.")
            return redirect('loginpage')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'register.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been confirmed. You can now login.')
        return redirect('loginpage')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('home')


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = authenticate(request, username=username, password=password)
        if username is not None:
            login(request, username)
            print(request.get_full_path())
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    template = loader.get_template('login.html')
    return render(request, "login.html")


def logoutuser(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url='loginpage')
def service1(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service1.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service1')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme,
              }
    return render(request, "service1.html", data)

@login_required(login_url='loginpage')
def service2(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service2.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service2')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme}
    return render(request, "service2.html", data)


@login_required(login_url='loginpage')
def service3(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service3.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service3')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme}
    return render(request, "service3.html", data)


@login_required(login_url='loginpage')
def service5(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service5.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service5')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme}
    return render(request, "service5.html", data)


@login_required(login_url='loginpage')
def service6(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service6.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service6')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme}
    return render(request, "service6.html", data)

@login_required(login_url='loginpage')
def service7(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service7.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service7')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme}
    return render(request, "service7.html", data)

@login_required(login_url='loginpage')
def service8(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service8.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service8')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme}
    return render(request, "service8.html", data)





@login_required(login_url='loginpage')
def service4(request):
    color_scheme =  Features.objects.get().color_schem
    template = loader.get_template('service4.html')
    serviceData = service.objects.all()
    service_obj= service.objects.get(service_url='service4')
    service_description = service_categoreis.objects.filter(name=service_obj)
    addressData = address.objects.all()
    data = {'addressData': addressData, "serviceData":serviceData,
             "service_description":service_description,
              "color_scheme":color_scheme}
    return render(request, "service4.html", data)



from django.shortcuts import render
from django.core.paginator import Paginator


# def blogs(request):
#     # Retrieve the color scheme safely
#     color_scheme = Features.objects.get().color_schem

#     # Initial post retrieval
#     posts = Post.objects.all()

#     # Filtering based on search query
#     filter = request.GET.get('search')
#     if filter:
#         posts = posts.filter(title__icontains=filter)

#     # Paginate the posts (after filtering, if any)
#     paginator = Paginator(posts, 4)  # Show 4 posts per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Gather tag data
#     tag_data = tagdata()
#     all_tags = list(set(tag for post in Post.objects.all() for tag in post.tags.all()))

#     # Retrieve address data
#     addressData = address.objects.all()

#     # Prepare context
#     data = {
#         'addressData': addressData,
#         'Post': page_obj,  # Only show the current page of posts
#         'all_tags': all_tags,
#         'tag_data': tag_data,
#         'page_obj': page_obj,
#         'color_scheme': color_scheme
#     }

#     return render(request, "blog-new.html", data)


def blogs(request):
    # Safely get the color scheme (avoid crash if Features table is empty)
    color_scheme = "default"
    try:
        feature = Features.objects.first()
        if feature:
            color_scheme = feature.color_schem
    except Exception:
        pass  # Table might not exist yet during initial migrations

    # Initial queryset for posts
    posts = Post.objects.all().order_by('-id')

    # Apply search filter (if provided)
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    # Apply pagination (after filtering)
    paginator = Paginator(posts, 4)  # 4 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tag_data = tagdata()

    # Gather unique tag data efficiently
    all_tags = set()
    for post in page_obj:
        all_tags.update(post.tags.all())

    # Retrieve address data
    addressData = address.objects.all()

    # Prepare template context
    context = {
        'addressData': addressData,
        'Post': page_obj,        # paginated posts
        'page_obj': page_obj,    # pagination object for template
        'all_tags': all_tags,
        'tag_data': tag_data,

        'color_scheme': color_scheme,
    }

    return render(request, "blog-new.html", context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog_detail', blog_id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', blog_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

def blogsfilter(request, tag_id):
    color_scheme =  Features.objects.get().color_schem
    tag_data = tagdata()
    # model = Post.objects.all()
    # ID = TaggedItem.objects.filter(object_id=blog_id).values_list('tag_id')
    print(tag_id)
    color_scheme =  Features.objects.get().color_schem
    all_tags = [tag for tag in Post.tags.filter()]
    model = Post.objects.filter(tags=tag_id)
    print(model)
    addressData = address.objects.all()
    data = {'addressData': addressData, 'page_obj': model,
            "all_tags": all_tags, "tag_data": tag_data, 
            "color_scheme" :color_scheme}
    return render(request, "blog-new.html", data)


def blog_detail(request, blog_id):
    color_scheme =  Features.objects.get().color_schem
    tag_data = tagdata()
    model = Post.objects.filter(pk=blog_id)
    all_tags = [tag for tag in Post.tags.filter()]
    blog = get_object_or_404(Post, id=blog_id)
    comments_count = Comment.objects.filter(post_id=blog_id).count()
    ID = TaggedItem.objects.filter(object_id=blog_id).values_list('tag_id')
    tags = []
    all_tags = [tag for tag in Post.tags.filter()]

    for id in ID:
        tag = [tag.name for tag in Post.tags.filter(id=id[0])]
        tags.append(tag[0])
    comments = blog.comments.all()
    comment_form = CommentForm()
    reply_form = ReplyForm()
    return render(request, 'blog-details.html', {'blog': blog, 'comments': comments, "color_scheme":color_scheme,
                  'comment_form': comment_form, 'reply_form': reply_form,
                                                 "Post": model, "comments_count": comments_count, "tags": tags, "all_tags": all_tags, 'tag_data': tag_data

                                                 })

# views.py

@login_required(login_url='loginpage')
def add_comment(request, blog_id):
    blog = get_object_or_404(Post, id=blog_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = blog
            comment.user = request.user
            comment.save()
    return redirect('blog_detail', blog_id=blog_id)


@login_required(login_url='loginpage')
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.post = comment
            reply.user = request.user
            reply.save()
    return redirect('blog_detail', blog_id=comment.post.id)

@login_required(login_url='loginpage')
def add_like(request, blog_id):
    blog = get_object_or_404(Post, id=blog_id)
    if request.user.id:
        like, created = Like.objects.get_or_create(
            post=blog, user=request.user)
        if not created:
            like.delete()
    else:
        return HttpResponse('You ned to login first to like this post')
    return redirect('blog_detail', blog_id=blog_id)




def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:  # Check if the subscriber is newly created
                subscriber.save()  # Save the subscriber if it's new
            return render(request, 'thank_you.html')  # Display a thank you page
    else:
        form = NewsletterSubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})

# models.py

from django.db.models.signals import post_save
from django.dispatch import receiver


# Signal handler to send newsletters when a new blog post is added
@receiver(post_save, sender=Post)
def send_newsletter_on_new_post(sender, instance, created, **kwargs):
    pass
    # if created:
    #     subscribers = NewsletterSubscriber.objects.all()
    #     blog_post = instance

    #     for subscriber in subscribers:
    #         send_mail(
    #             'New Blog Post Alert',
    #             f'A new blog post titled "{blog_post.title}" has been added. Check it out at: example.com/blog/',
    #             'sender@example.com',  # Your sender email address
    #             [subscriber.email],
    #             fail_silently=False,
    #         )
            

# This code assumes you have a model named NewsletterSubscriber with an 'email' field to store subscribers' email addresses.


from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author == request.user or request.user.is_staff:
            post.delete()
        return redirect('home')

class DeleteCommentView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user or request.user.is_staff:
            post_id = comment.post.id
            comment.delete()
            return redirect('post_details',post_id=post_id )
   
def post_detail(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        return render(request, 'blog_details.html', {'post': post})

class DeleteReplyView(LoginRequiredMixin, View):
    def post(self, request, reply_id):
        reply = get_object_or_404(Reply, id=reply_id)
        comment_id = reply.post.id
        post_id = reply.post.post.id
        if reply.user == request.user or request.user.is_staff:
            reply.delete()
        return redirect('post_details', post_id=post_id)

