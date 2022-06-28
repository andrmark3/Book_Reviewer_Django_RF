from django.urls import path
from . import views

urlpatterns =[
    # // Part 1 // Searching functionallity from url kwargs.  
    path("external/", views.GutendexList.as_view()),
    # // Part 1 // Searching functionallity from searching param.                                    
    path("external/<str:search>/", views.GutendexList.as_view()),
    # // Part 1 // + Pagination                       
    path("external/<int:page>/", views.GutendexList.as_view()),
    # // Part 2 //                         
    path("review/<int:book_id>/", views.GutendexRetrieveCreate.as_view()),
    # // Part 3 //                                               
    path("book/<int:book_id>/", views.DetailBookView.as_view()),   
    # // Bonus average service by book_id and year.
    # TODO: optimize and sorten the logic of code.                                   
    path("average_month/<int:book_id>/", views.AverageMonthServiceBookView.as_view()),                
    path("average_month/<int:book_id>/<int:year>/", views.AverageMonthServiceBookView.as_view()),                
    # // Bonus top books service
    # TODO: optimize and sorten the logic of code.                                                  
    path("top_books/<int:top_num>/", views.TopBooksServiceBookView.as_view()),   
]

