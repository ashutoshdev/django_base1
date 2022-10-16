from django.conf import settings
from django.db import models


class AbstractModel(models.Model):
    """

    """
    created_at = models.DateTimeField(
        verbose_name='Created At', auto_now_add=True)
    modified_at = models.DateTimeField(
        verbose_name='Modified At', auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_%(class)s_set',
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Created By")
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='updated_%(class)s_set',
        on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Modified By")

    class Meta:
        abstract = True
