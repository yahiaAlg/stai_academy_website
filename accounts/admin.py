from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import *

# Register your models here.
class AnouncementAdmin(admin.ModelAdmin):
    list_display = ["id", "designer_profile", "title", "description", "date_created"]
    list_editable = ["designer_profile"]
    list_display_links = ["id","title"]
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        user_designer_profile = Designer.objects.filter(owner=request.user).first()
        qs =  super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(designer_profile=user_designer_profile)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ["id","teacher","student", "date_sent"]
    list_display_links = ["student"]
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["owner","bio","role"]
    list_filter = ["role"]


class GaurdianshipAdmin(admin.ModelAdmin):
    list_display = ["id","parent","student", "date_assigned"]

admin.site.register(Designer)
admin.site.register(Anouncement, AnouncementAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Departement)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Gaurdianship, GaurdianshipAdmin)
