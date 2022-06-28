from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AbstractBaseModel
from core.mixins import AutoFieldPrimaryKey, TimeStampsMixin, CreatedTimeStampMixin


# ======================================================================================================================
class BookReview(AbstractBaseModel, AutoFieldPrimaryKey, CreatedTimeStampMixin):
    """
        Book Review model for returning the reviews and the date that are created.
    """
    # ------------------------------------------------------------------------------------------------------------------
    book_id=models.IntegerField(default=None, null=False)
    score= models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    description= models.CharField(max_length=250, null=True, blank=True)

    # ------------------------------------------------------------------------------------------------------------------
    class Meta:
        db_table= 'book_reviews'
        ordering = ['id',]

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.id}"

# ======================================================================================================================
