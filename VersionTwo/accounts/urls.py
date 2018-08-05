from . import views
from django.urls import path
from django.views.generic.base import RedirectView


app_name = 'accounts'
urlpatterns = [
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', RedirectView.as_view(pattern_name='accounts:signin'), name='login'),
    path('logout/', RedirectView.as_view(pattern_name='accounts:signout'), name='logout'),
    path('registration/', RedirectView.as_view(pattern_name='accounts:signup'), name='registration'),
]
