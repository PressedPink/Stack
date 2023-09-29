from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include
from django.views.generic import RedirectView

import base

from Stack.views import login, signup, tasks, dbTask

urlpatterns = [
    path('', include('pwa.urls')),
    path('', login.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('signup/', signup.as_view(), name='signup'),
    path('tasks/', tasks.as_view(), name='tasks'),
    path('dbTask/', dbTask.as_view(), name='manageTasks'),
]