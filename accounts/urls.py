from django.urls import path
from .views import signup
from .views import signin
from .views import dashboard
from .views import hives
from .views import subscription
from .views import profile
from .views import logout
from .views import settings
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path("signup/", signup, name="signup"),
    path('signin/', signin, name='signin'),
    path('dashboard/', dashboard, name='dashboard'),
    path('hives/', hives, name='hives'),
    path('subscription/', subscription, name='subscription'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('logout/', logout, name='logout'),
    path('index/', views.index, name='index'),
    path('pay/', views.pay_subscription, name='pay_subscription'),
]
