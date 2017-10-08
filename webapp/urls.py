from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from instagram import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^instagram/', include('instagram.urls')), #url for the user page directs you to the applications url file
    url(r'^$', views.home, name="home1")  #url for the viewer page
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
