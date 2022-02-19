from django import forms

from .models import Comment, Contact, Post

class CommentForm(forms.ModelForm):
    """Class represents comment form."""

    class Meta:
        model = Comment
        fields = ["text"]
        labels =  {
            "text": "Your Comment"
        }

class ContactForm(forms.ModelForm):
    """Class represents contact form."""

    class Meta:
        model = Contact
        fields = "__all__"
        labels = {
            "first_name": "Your first name",
            "last_name": "Your last name",
            "email": "Your email",
            "message": "Message's text"
        }

class PostForm(forms.ModelForm):
    """Class represents post form."""

    class Meta:
        model = Post
        fields = ["title", "description", "content", "image", "tags"]