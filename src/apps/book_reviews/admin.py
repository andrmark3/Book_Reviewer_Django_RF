from django.contrib import admin
from .models import BookReview


class BookReviewAdmin(admin.ModelAdmin):
    # fields = ('id',)
    list_display= ('id',)

admin.site.register(BookReview,BookReviewAdmin)



