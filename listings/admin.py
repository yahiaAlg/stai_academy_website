from django.contrib import admin
from .models import Listing,Anouncement


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "is_published",
        "price",
        "list_date",
        "instructor",
    )
    list_display_links = (
        "id",
        "title",
        "list_date",
    )
    list_filter = ("title", "list_date")
    list_editable = ("is_published", "price")
    search_fields = ("title", "description", "list_date", "price")

# Register your models here.
class AnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "event_date",
    )
    list_display_links = (
        "id",
        "title",
        "event_date",
    )


admin.site.register(Listing, ListingAdmin)
admin.site.register(Anouncement,AnouncementAdmin)
