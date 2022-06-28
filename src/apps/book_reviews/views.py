import requests
from django.http import Http404, HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets,mixins,generics
from .models import BookReview
from .serializers import BookReviewsSerializer,CreateBookReviewsSerializer
from rest_framework.response import Response



# =================================================================================================================================================
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



# =================================================================================================================================================
class GutendexList(generics.ListAPIView):
    """
    Search author names and book titles with given words. For example, /?search=dickens+great includes Great Expectations by Charles Dickens.
    """
    serializer_class = CreateBookReviewsSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['title','authors',]

    # GET /api/books/external/ 
    # GET /api/books/external/?search=dickens+great 
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    """ Getting a list of all books or with a serach term of title or author.
    """
    #------------------------------------------------------------------------------------------------
    def get_queryset(self, page=None):
        try:
            page = self.kwargs.get('page')
            search = self.kwargs.get('search')
            search_param = self.request.query_params.get('search')
            if page is None:
                page = 1
            if search == None and search_param == None:
                r = requests.get(f'https://gutendex.com/books/?page={page}')
                api_data = r.json()['results']
                transformed_data = gutendex_transfrom(api_data)
                return transformed_data['books']
            else:
                if search_param is not None:
                    search=search_param
                r = requests.get(f'https://gutendex.com/books/?search={search}%20{search}')
                api_data = r.json()['results']
                transformed_data = gutendex_transfrom(api_data)
                return transformed_data['books']
        except BookReview.DoesNotExist:
            raise Http404

    #------------------------------------------------------------------------------------------------
    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        return Response(instance)
        

# =================================================================================================================================================
class GutendexRetrieveCreate(generics.RetrieveAPIView,generics.CreateAPIView):
    """ Retrieve a single detail book for creating reviews.
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
            r = requests.get(f'https://gutendex.com/books?ids={book_id}')
            api_data = r.json()['results']
            transformed_data = gutendex_transfrom(api_data)
            return transformed_data
        except BookReview.DoesNotExist:
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
    serializer_class = CreateBookReviewsSerializer
    queryset = BookReview.objects.all()

    #------------------------------------------------------------------------------------------------
    def detail_book_transfrom(self,api_data, data):
        def average(lst):
            if lst == []:
                return lst
            return sum(lst) / len(lst)
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
    def get_object(self, book_id):
        try: 
            # External api request.
            r = requests.get(f'https://gutendex.com/books?ids={book_id}')
            api_data = r.json()['results']
            # Fetching BookReviews from Database.
            book=BookReview.objects.filter(book_id=book_id)
            serializer = BookReviewsSerializer(book , many=True)

            transformed_data = self.detail_book_transfrom(api_data, serializer.data)
            return transformed_data
        except BookReview.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        try:
            book_id = self.kwargs.get('book_id')
            instance = self.get_object(book_id)
            return Response(instance) 
        except Exception:
            return Http404 

    # def perform_create(self, serializer,id:int):
    #     # Extend and mutating the values before saving to serializer.
    #     book_id = serializer.data.get('book_id')
    #     if book_id == None:
    #         book_id=id
    #     description = serializer.data.get('description')

    #     # Serialize and save to the database.
    #     book_serializer = CreateBookReviewsSerializer(data=serializer.data)
    #     book_serializer.is_valid(raise_exception=True)
    #     book_serializer.save(book_id=book_id,description=description)

    #     return book_serializer

    # #------------------------------------------------------------------------------------------------
    # def create(self, request, *args, **kwargs):
    #     book_id = self.kwargs['book_id']
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     ser = self.perform_create(serializer,book_id)
    #     headers = self.get_success_headers(serializer.data)
    #     instance = self.get_object(book_id)
    #     return Response(instance, status=status.HTTP_201_CREATED, headers=headers)

# =================================================================================================================================================