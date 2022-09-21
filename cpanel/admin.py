from django.contrib import admin
from dashboard import models

# Register your models here.


class article(admin.ModelAdmin):
    model: models.article
    list_display = (
        "article_id",
        "article_title",
        "category",
        "views",
        "likes",
        "success_ratio",
        "created_at",
    )


admin.site.register(models.article, article)
