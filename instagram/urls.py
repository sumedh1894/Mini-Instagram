from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from webapp import settings

#all URLs are directed here after looking up in the project URLs folder except the admin account

app_name='instagram'
urlpatterns = [
    url(r'^$', views.homepage, name='home'),
    url(r'login/', views.login1, name='login'),
    url(r'signup/', views.signup, name='signup'),
    url(r'logout/', views.logout1, name='logout'),
    url(r'delete/', views.delete, name='delete'),
    url(r'edit/', views.edit, name='edit'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)