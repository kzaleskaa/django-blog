from django.contrib.auth.models import User
from django.urls import resolve
from django.test import TestCase, Client
from blog.views import *
from blog.models import *

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='admin', password='pass@123', email='admin@admin.com')
        self.tag = Tag.objects.create(tag_name="new")
        self.post = Post.objects.create(title="title", description="description", content="content", image="test.jpg", user=self.user)
        self.post.tags.add(self.tag)

    def test_resolve_to_home_page_view(self):
        resolver = resolve("/")
        self.assertEqual(resolver.func.__name__, StartingPageView.as_view().__name__)
    
    def test_resolve_to_all_post_page_view(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, AllPostsView.as_view().__name__)

    def test_resolve_to_contact_page_view(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ContactPageView.as_view().__name__)

    def test_resolve_to_saved_page_view(self):
        response = self.client.get('/saved/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, SavedPostView.as_view().__name__)

    def test_resolve_to_signup_page_view(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, SignupView.as_view().__name__)

    def test_resolve_to_signin_page_view(self):
        response = self.client.get('/signin/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, SigninView.as_view().__name__)

    def test_resolve_to_profile_page_view(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ProfileView.as_view().__name__)

    def test_resolve_to_details_page_view(self):
        response = self.client.get(reverse('post-detail', args=(self.post.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, PostDetailsView.as_view().__name__)
