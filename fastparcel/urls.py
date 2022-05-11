from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views
from django.conf import settings
from django.conf.urls.static import static

from core.customer import views as customer_views
from core.courier import views as courier_views

customer_urlpatterns = [
    path('', customer_views.home, name='home'),
    path('profile/', views.home, name='home'),

]

courier_urlpatterns = [
    path('', courier_views.home, name='home')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', views.profile),

    path('schedule_list/', views.schedule_list),
    path('route_recommend/', views.route_recommend),
    path('home/', views.home),

    path('', views.home),
    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('courier/', include((courier_urlpatterns, 'courier'))),

    path('', include('social_django.urls', namespace='social')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
