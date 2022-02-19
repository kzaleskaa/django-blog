from django.contrib.auth.models import User
from django.test import TestCase
from blog.forms import *
from blog.models import Tag

class CommentFormTest(TestCase):
    def test_valid_form(self):
        data = {'text': 'text'}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'text': ''}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

class ContactFormTest(TestCase):
    def test_valid_form(self):
        data = {'first_name': 'John', 'last_name': 'Smith', 'email': 'john@gmail.com', 'message': 'Problem with profile page.', 'topic': "posts"}
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'first_name': '', 'last_name': 'Smith', 'email': '', 'message': 'Problem with profile page.'}
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        
