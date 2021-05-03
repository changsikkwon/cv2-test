from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "image"
        verbose_name = "이미지"
        verbose_name_plural = verbose_name
