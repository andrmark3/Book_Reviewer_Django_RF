
from django.db import models


# ======================================================================================================================
class AbstractBaseModel(models.Model):
    """
    A base model which other data models should inherit from to gain common fields and functionality

    Add any common functionality or attributes here
    """

    class Meta:
        abstract = True
# ======================================================================================================================

