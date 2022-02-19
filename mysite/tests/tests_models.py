from django.test import TestCase
from blog.models import Tag, Comment, Contact, Post
from django.contrib.auth.models import User

class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag(tag_name="new")

    def test_tag_creation(self):
        self.tag.save()
        self.assertTrue(isinstance(self.tag, Tag))
        self.assertEqual(self.tag.__str__(), self.tag.tag_name)    

class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='pass@123', email='admin@admin.com')
        self.tag = Tag.objects.create(tag_name="new")
        self.post = Post.objects.create(title="title", description="description", content="content", image="test.jpg", user=self.user)
        self.post.tags.add(self.tag)
        self.comment = Comment(user=self.user, text="It's okay.", post=self.post)
        
    def test_comment_creation(self):
        self.comment.save()
        self.assertTrue(isinstance(self.comment, Comment))

class ContactModelTestCase(TestCase):
    def setUp(self):
        self.contact = Contact(first_name="John", last_name="Smith", email="john@gmail.com", topic="COOPERATION", message="Problem with my profile page.")

    def test_contact_creation(self):
        self.contact.save()
        self.assertTrue(isinstance(self.contact, Contact))


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin', password='pass@123', email='admin@admin.com')
        self.tag = Tag.objects.create(tag_name="new")
        self.post = Post(title="title", description="description", content="content", image="test.jpg", user=self.user)

    def test_post_creation(self):
        self.post.save()
        self.post.tags.add(self.tag)
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.__str__(), self.post.title)   
