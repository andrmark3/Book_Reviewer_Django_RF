from django.db import models



"""
Common mixins for repeatable fields.
"""
# ======================================================================================================================
class AutoFieldPrimaryKey(models.Model):
    """
        Auto primary key field for models
    """

    class Meta:
        abstract = True

    # ------------------------------------------------------------------------------------------------------------------
    id = models.AutoField(primary_key=True, auto_created=True)


# ======================================================================================================================
class TimeStampsMixin(models.Model):
    """
        Created and Modified timestamp fields for models
    """

    class Meta:
        abstract = True

    # ------------------------------------------------------------------------------------------------------------------
    created = models.DateTimeField(auto_now_add=True, null=False)
    modified = models.DateTimeField(auto_now=True, null=False)


# ======================================================================================================================
class CreatedTimeStampMixin(models.Model):  # asdasdasdasdasd
    """
        Created timestamp field only for models - use on write once read many fields, such as imported scores
    """

    class Meta:
        abstract = True

    # ------------------------------------------------------------------------------------------------------------------
    created = models.DateTimeField(auto_now_add=True, null=False)


# ======================================================================================================================

