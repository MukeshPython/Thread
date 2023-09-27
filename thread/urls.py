from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('concurrent/', views.Concurrent.as_view()),
    path('asyncio/', views.Asyncio.as_view(), name= 'asyncio'),
    path('multiprocessing/', views.Multiprocessing.as_view()),
    path('aiohttp/', views.Aiohttp.as_view()),
    path('httpx/', views.Httpx.as_view())
]