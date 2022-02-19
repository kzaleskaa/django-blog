from django.urls import path

from . import views 

# Create url patterns.

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts/", views.AllPostsView.as_view(), name="all-posts-page"),
    path("contact/", views.ContactPageView.as_view(), name="contact-page"),
    path("saved/", views.SavedPostView.as_view(), name="saved-page"),
    path("posts/<slug:slug>/", views.PostDetailsView.as_view(), name="post-detail"),
    path("signup/", views.SignupView.as_view(), name="signup-page"),
    path("signin/", views.SigninView.as_view(), name="signin-page"),
    path("profile/", views.ProfileView.as_view(), name="profile-page"),
    path("signout/", views.signout, name="signout-page"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("delete/<event_id>/", views.delete, name="delete-post"),
    path("delete/<event_id>/<slug:slug>/", views.delete_comment, name="delete-comment")
]
