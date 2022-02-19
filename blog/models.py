from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
    """Class represents tag in database."""

    tag_name = models.CharField(max_length=25)

    def __str__(self):
        return self.tag_name

class Post(models.Model):
    """Class represents post in database."""

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    content = models.TextField(validators=[MinLengthValidator(5)])
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def latest_post_pk(self):
        object_pk = Post._default_manager.latest('pk')
        new_pk = object_pk.pk + 1
        return new_pk
    
    def save(self, *args, **kwargs):
        latest_post_key = ""

        try: 
            latest_post_key = self.latest_post_pk()
        except Exception:
            latest_post_key = ""

        self.slug = slugify(f"{self.title} {latest_post_key}")
        return super().save(*args, **kwargs)

class Comment(models.Model):
    """Class represents comment in database."""

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

class Contact(models.Model):
    """Class represents contact in database."""

    TOPIC_CHOICES = [
        ("cooperation", ("Interested to cooperation")),
        ("social media", ("Information about social media")),
        ("posts", "Comment to posts"),
        ("another", "Another topic")
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    topic = models.CharField(max_length=40, choices=TOPIC_CHOICES, default="cooperation")
    message = models.TextField(validators=[MinLengthValidator(5)])
    