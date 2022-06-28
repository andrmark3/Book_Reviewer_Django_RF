from django.urls import path
from django.db import router
from rest_framework import routers
from . import views
from django.urls import include

router = routers.DefaultRouter()
urlpatterns =[  
    path("external/", views.GutendexList.as_view()),                       # // Part 1 // Searching functionallity from url kwargs.
    path("external/<str:search>/", views.GutendexList.as_view()),           # // Part 1 // Searching functionallity from searching param.
    path("external/<int:page>/", views.GutendexList.as_view()),            # // Part 1 // + Pagination
    path("review/<int:book_id>/", views.GutendexRetrieveCreate.as_view()),  # // Part 2 //                                 
    path("book/<int:book_id>/", views.DetailBookView.as_view()),           # // Part 3 //                
]
urlpatterns += router.urls
