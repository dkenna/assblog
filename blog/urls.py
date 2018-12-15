from django.urls import path, re_path
from api.views import article, articles 
from api.views import get_404

urlpatterns = [
    re_path('^art/(?P<pk>\d+)/?$', article),
    re_path('^art/?$', article),
    re_path('^arts/?$', articles),
    re_path('^', get_404)
]
