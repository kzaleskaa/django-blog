from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from mysite import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .tokens import generate_token
from .models import Post, Comment
from .forms import CommentForm, ContactForm, PostForm

# Create your views here.

class StartingPageView(View):
    """"Class represents main page, derived from the View class."""

    def get(self, request):
        posts = Post.objects.order_by("-date")[:3]
        user = request.user

        context = {
            "all_posts": posts,
            "user": user
        }

        return render(request, "blog/index.html", context)

class ProfileView(View):
    """"Class represents user's profile, derived from the View class."""

    def get(self, request):
        user = request.user
        posts = Post.objects.all().filter(user=user)

        context = {
            "user": user,
            "post_form": PostForm(),
            "posts": posts
        }

        return render(request, "blog/profile.html", context)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "You added new post!")
            return redirect("profile-page")
        
        return HttpResponseRedirect("/")

class AllPostsView(ListView):
    """"Class represents all posts page, derived from the ListView class."""

    template_name = "blog/all_posts.html"
    model = Post
    context_object_name = "all_posts"

class PostDetailsView(View):
    """"Class represents post's detail page, derived from the View class."""
    
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "saved_for_later": self.is_stored_post(request, post.id),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }

        return render(request, "blog/post.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse("post-detail", args=[slug]))

        return render(request, "blog/post-detail.html")

class SavedPostView(View):
    """"Class represents saved post page, derived from the View class."""

    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/saved.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")

class ContactPageView(View):
    """"Class represents contact page (user can post any question/problem), derived from the View class."""

    def get(self, request):
        context = {
            "contact_form": ContactForm(),
        }
        return render(request, "blog/contact.html", context)
        
    def post(self, request):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.save()
            return HttpResponseRedirect("/")


class SignupView(View):
    """"Class represents signup page, derived from the View class."""

    def get(self, request):
        return render(request, "blog/authentication/signup.html")

    def post(self, request):
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            failed = "Username already exists! Please try some other username."
            # return HttpResponse(failed)
            return JsonResponse({"status": "error", "msg": failed})

        if User.objects.filter(email=email):
            failed = "Email already registered"
            return JsonResponse({"status": "error", "msg": failed})

        if pass1 != pass2:
            failed = "Password didn't match!"
            return JsonResponse({"status": "error", "msg": failed})

        if not username.isalnum():
            failed = "Username must be Alpha-Numeric!"
            return JsonResponse({"status": "error", "msg": failed})

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        # Send Welcome Email

        subject = "Welcome to Django Blog"
        message = "Hello " + myuser.first_name + "!\n\nThank you for visiting website. \nWe have also sent you a confirmation email, please confirm email in order to activate your account. \nThank you!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Send Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm You Email - Django Blog"
        message2 = render_to_string("blog/email_confirmation.html", {
            'name': myuser.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token": generate_token.make_token(myuser)
        })

        email = EmailMessage(email_subject, message2, from_email, to_list)

        email.fail_silently = True

        email.send()
            
        success = f"Hello {username}! Your account was created, check your email and click received link to activate your account."
        return JsonResponse({"status": "success", "msg": success})

class SigninView(View):
    """"Class represents signin page, derived from the View class."""

    def get(self, request):
        return render(request, "blog/authentication/signin.html")

    def post(self, request):
        username = request.POST['username'] 
        pass1 = request.POST['pass']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect("starting-page")
        else: 
            messages.error(request, "Bad credentials. Try again.")
            return render(request, "blog/authentication/signin.html")


def signout(request):
    """"Logout user."""

    logout(request)
    return redirect("starting-page")


def activate(request, uidb64, token):
    """Function tries to activate user's account."""
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect("starting-page")
    else:
        return render(request, "blog/activation_failed.html")

def delete(request, event_id):
    """Function deletes user's post."""

    post = Post.objects.get(pk=event_id)
    post.delete()
    return redirect("profile-page")

def delete_comment(request, event_id, slug):
    """Function deletes user's comment."""

    comment = Comment.objects.get(pk=event_id)
    comment.delete()
    return HttpResponseRedirect(reverse("post-detail", args=[slug]))
