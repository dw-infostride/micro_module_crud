"""m3s URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crud import views
from django.conf.urls.static import static
from m3s import settings
from django.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start_page, name='start_page' ),
    path('sign-up/', views.sign_up, name='sign_up' ),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.log_out, name="logout"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('change-password/', views.change_password, name="change_password"),
    path('delete-user/', views.delete_user, name="delete_user"),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('change-password/<token>/', views.reset_password , name = 'change_password')

    

    


    
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
