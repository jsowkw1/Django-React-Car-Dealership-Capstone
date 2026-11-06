from django.contrib import admin
from django.urls import include, path, re_path

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from djangoapp.views import frontend

admin.site.site_header = 'Car Dealership Administration'
admin.site.site_title = 'Car Dealership Admin'
admin.site.index_title = 'Dealership data management'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    # Static HTML pages: frontend/static/About.html and Contact.html
    path('about', ensure_csrf_cookie(TemplateView.as_view(template_name='About.html')), name='about'),
    path('contact', ensure_csrf_cookie(TemplateView.as_view(template_name='Contact.html')), name='contact'),
    # Every other path is a React Router page served from the production build.
    path('', frontend, name='home'),
    re_path(r'^(?:login|register|dealers|dealer|postreview)(?:/.*)?/?$', frontend),
]
