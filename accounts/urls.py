from django.urls import path
from .views import signup
from .views import signin
from .views import dashboard
from .views import hives
from .views import subscription
from .views import profile
from .views import save_token
from .views import logout
from .views import settings
from .views import password_reset
from .import views
from django.conf.urls.static import static
from django.views.generic import TemplateView

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
    path('reset_password/', views.password_reset, name='reset_password'),
    path('save-token/', views.save_token, name='save_token'),
    path('api/initiate_payment/', views.initiate_payment, name='initiate_payment'),
]
