from datetime import date
import requests
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics,viewsets,mixins
from .models import BookReview
from .serializers import BookReviewsSerializer,CreateBookReviewsSerializer
from rest_framework.response import Response

#------------------------------------------------------------------------------------------------
# Average functionality.
def average(lst):
    if lst == []:
        return 0
    return sum(lst) / len(lst)
#------------------------------------------------------------------------------------------------
""" Transformation function of Gutendex response data.
"""
def gutendex_transfrom(obj):
    try:
        response=dict({
            'books':[dict({
            'id':int(item['id']),
            'title':str(item['title']),
            'authors':[dict(**author) for author in item['authors']],
            'languages':list([str(language) for language in item['languages']]),
            'download_count':int(item['download_count']),
            }) for item in obj]
        })
        return response
    except Exception:
        return {f"Wrong data inserted in the function 'gutendex_transfrom'"} 

#------------------------------------------------------------------------------------------------



# =================================================================================================================================================
class GutendexList(generics.ListAPIView):
    """
    Search author names and book titles with given words. For example, /?search=dickens+great includes Great Expectations by Charles Dickens.
    """
    serializer_class = CreateBookReviewsSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['title','authors',]

    # GET /api/books/external/   //Fetch all books from Gutendex
    # GET /api/books/external/2   //Pagination
    # GET /api/books/external/dickens+great   //Search kwargs
    # GET /api/books/external/?search=dickens+great   //Search param
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    """ Getting a list of all books or with a serach term of title or author.
    """
    def get_queryset(self, page=None):
        try:
            # Getting kwargs from url.
            page = self.kwargs.get('page')
            search = self.kwargs.get('search')
            search_param = self.request.query_params.get('search')
            if page is None:
                page = 1
            if search == None and search_param == None:
                # External api request. 
                r = requests.get(f'https://gutendex.com/books/?page={page}')
                api_data = r.json()['results']

                # Transformation of api data.
                transformed_data = gutendex_transfrom(api_data)
                return transformed_data['books']
            else:
                if search_param is not None:
                    search=search_param
                # External api request.
                r = requests.get(f'https://gutendex.com/books/?search={search}%20{search}')
                api_data = r.json()['results']

                # Transformation of api data.
                transformed_data = gutendex_transfrom(api_data)
                return transformed_data['books']
        except Exception:
            raise Http404

    #------------------------------------------------------------------------------------------------
    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        return Response(instance)
        

# =================================================================================================================================================
class GutendexRetrieveCreate(generics.RetrieveAPIView,generics.CreateAPIView):
    """ Retrieve a single detail of Gutendex book for creating a review on his id.
    """
    serializer_class = CreateBookReviewsSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['title','id']

    # GET /api/books/review/<int:book_id>
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    """ Retrieve a single book from Gutendex API by id.
    """
    #------------------------------------------------------------------------------------------------
    def get_object(self, book_id):
        try:
            # External api request.
            r = requests.get(f'https://gutendex.com/books?ids={book_id}')
            api_data = r.json()['results']

            #Transformation of api data
            transformed_data = gutendex_transfrom(api_data)
            return transformed_data
        except Exception:
            raise Http404
        
    #------------------------------------------------------------------------------------------------
    def retrieve(self, request, *args, **kwargs):
        book_id = self.kwargs['book_id']
        instance = self.get_object(book_id)
        return Response(instance)  


    # POST /api/books/review/<int:book_id> 
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #------------------------------------------------------------------------------------------------
    """ Creating a new review for the retrieved book.
    """
    def perform_create(self, serializer,id:int):
        # Extend and mutating the values before saving to serializer.
        book_id = serializer.data.get('book_id')
        if book_id == None:
            book_id=id
        description = serializer.data.get('description')

        # Serialize and save to the database.
        book_serializer = CreateBookReviewsSerializer(data=serializer.data)
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save(book_id=book_id,description=description)
        return book_serializer

    #------------------------------------------------------------------------------------------------
    def create(self, request, *args, **kwargs):
        book_id = self.kwargs['book_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ser = self.perform_create(serializer,book_id)
        headers = self.get_success_headers(serializer.data)
        return Response(ser.data, status=status.HTTP_201_CREATED, headers=headers)
    

# =================================================================================================================================================
class DetailBookView(generics.RetrieveAPIView):
    """ Retrieve a detail view of book, by merging data from Gutendex and reviews from db.
    """
    serializer_class = CreateBookReviewsSerializer
    queryset = BookReview.objects.all()

    #------------------------------------------------------------------------------------------------
    def detail_book_transfrom(self,api_data, data):
        try:
            response=[dict({
                'id':int(item['id']),
                'title':str(item['title']),
                'authors':[dict(**author) for author in item['authors']],
                'languages':list([str(language) for language in item['languages']]),
                'download_count':int(item['download_count']),
                'rating':average([item['score'] for item in data]),  # Getting all the score values and calculate average score.
                'reviews':filter(None,[item['description'] for item in data]),    # Getting all descriptions and filtering Null values.
                }) for item in api_data]
            return response
        except Exception:
            return {f"Wrong data inserted in the function 'gutendex_transfrom'"} 

    # GET /api/books/<int:book_id>
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #------------------------------------------------------------------------------------------------
    def get_object(self):
        try: 
            book_id = self.kwargs.get('book_id')
            # External api request.
            r = requests.get(f'https://gutendex.com/books?ids={book_id}')
            api_data = r.json()['results']

            # Fetching BookReviews from Database.
            book=BookReview.objects.filter(book_id=book_id)
            serializer = BookReviewsSerializer(book , many=True)

            # Transformation of serializer
            transformed_data = self.detail_book_transfrom(api_data, serializer.data)
            return transformed_data
        except Exception:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(instance) 

# =================================================================================================================================================
class AverageMonthServiceBookView(generics.RetrieveAPIView):
    """ A service that handles book_id and year and return the average scores by month.
    """

    # GET average/<int:book_id>/  
    # GET average/<int:book_id>/<int:year>/  
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #------------------------------------------------------------------------------------------------
    def get_object(self):
        try: 
            # External api request.
            book_id = self.kwargs.get('book_id')
            year = self.kwargs.get('year')
            if year is None:
                year = date.today().year

            # Fetching BookReviews from Database.
            book=BookReview.objects.filter(book_id=book_id)
            serializer = BookReviewsSerializer(book , many=True)
            sorted_by_year = list(filter(None,[data if data['created'][0:4] == str(year) else None for data in serializer.data]))
            month = dict({
                'January':average(list(filter(None,[data['score'] if data['created'][5:7] == '01' else None for data in sorted_by_year ]))),
                'February':average(list(filter(None,[data['score'] if data['created'][5:7] == '02' else None for data in sorted_by_year ]))),
                'March':average(list(filter(None,[data['score'] if data['created'][5:7] == '03' else None for data in sorted_by_year ]))),
                'April':average(list(filter(None,[data['score'] if data['created'][5:7] == '04' else None for data in sorted_by_year ]))),
                'May':average(list(filter(None,[data['score'] if data['created'][5:7] == '05' else None for data in sorted_by_year ]))),
                'June':average(list(filter(None,[data['score'] if data['created'][5:7] == '06' else None for data in sorted_by_year ]))),
                'July':average(list(filter(None,[data['score'] if data['created'][5:7] == '07' else None for data in sorted_by_year ]))),
                'August':average(list(filter(None,[data['score'] if data['created'][5:7] == '08' else None for data in sorted_by_year ]))),
                'September':average(list(filter(None,[data['score'] if data['created'][5:7] == '09' else None for data in sorted_by_year ]))),
                'October':average(list(filter(None,[data['score'] if data['created'][5:7] == '10' else None for data in sorted_by_year ]))),
                'November':average(list(filter(None,[data['score'] if data['created'][5:7] == '11' else None for data in sorted_by_year ]))),
                'December':average(list(filter(None,[data['score'] if data['created'][5:7] == '12' else None for data in sorted_by_year ]))),
            })
            return month
        except Exception:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(instance) 


# =================================================================================================================================================
class TopBooksServiceBookView(generics.RetrieveAPIView):
    """ Retrieve a detail view of book, by merging data from Gutendex and reviews from db.
    """
    serializer_class = CreateBookReviewsSerializer
    queryset = BookReview.objects.all()

    # GET /api/books/<int:book_id>
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #------------------------------------------------------------------------------------------------
    def detail_book_transfrom(self, data,serializer):
        try:
            for d in data:
                general_id = d['id']
                response=dict({
                    'id':int(d['id']),
                    'title':str(d['title']),
                    'authors':[dict(**author) for author in d['authors']],
                    'languages':list([str(language) for language in d['languages']]),
                    'download_count':int(d['download_count']),
                    'rating':average(list(filter(None,([item['score'] if item['book_id'] == general_id else None for item in serializer])))),  # Getting all the score values and calculate average score.
                    'reviews':list(filter(None,([item['description'] if item['book_id'] == general_id else None for item in serializer]))),    # Getting all descriptions and filtering Null values.
                    })
                return response
        except Exception:
            return {f"Wrong data inserted in the function 'gutendex_transfrom'"} 

    #------------------------------------------------------------------------------------------------
    def get_object(self):
        try: 
            # Getting top_num from url kwargs
            top_num = self.kwargs.get('top_num')

            # Fetching data from db.
            book=BookReview.objects.all()
            serializer = BookReviewsSerializer(book , many=True)
            ids = [id['book_id'] for id in serializer.data]
            sorted_ids = sorted(set(ids))

            # External api request
            api_data = []
            for id in sorted_ids:
                api_data.append(requests.get(f'https://gutendex.com/books?ids={id}').json())

            # Transformation of sorted data.
            transformed_books=[]
            for data in api_data:
                transformed_books.append(self.detail_book_transfrom(data['results'], serializer.data))

            # Gettig Scores and book_id.
            get_scores=sorted([(value['rating'],value['id']) for value in transformed_books],reverse=True)

            # Sorting books by scores.
            sorted_by_score = list(filter(None,[book if score[1] == book['id'] else None for score in get_scores for book in transformed_books]))

            # Sorting books by top_num from url kwargs.
            sorted_by_length = []
            length = top_num
            for book in sorted_by_score:
                length = length -1
                if length >= 0 :
                    sorted_by_length.append(book)
                pass        

            return sorted_by_length

        except Exception:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(instance) 


