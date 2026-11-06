from django.contrib import admin
from django.urls import include, path, re_path

from djangoapp.views import frontend

admin.site.site_header = 'Car Dealership Administration'
admin.site.site_title = 'Car Dealership Admin'
admin.site.index_title = 'Dealership data management'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    # Every other path is a React Router page served from the production build.
    path('', frontend, name='home'),
    re_path(r'^(?:about|contact|login|register|dealers|dealer|postreview)(?:/.*)?/?$', frontend),
]
