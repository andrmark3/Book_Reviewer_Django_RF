from rest_framework import serializers
from .models import BookReview


#==============================================================================================
class BookReviewsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BookReview
        fields = ('__all__')

#==============================================================================================
class CreateBookReviewsSerializer(serializers.ModelSerializer):
    book_id=serializers.IntegerField(help_text="Let it blank for auto assignment to current book retrieved.", required=False)
    score= serializers.IntegerField(help_text="Score review have to be integer (0-5).")
    description= serializers.CharField(help_text="Description review is optional.",required=False,)

    class Meta: 
        model = BookReview
        exclude = ('id',)

#==============================================================================================    