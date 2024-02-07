from django.shortcuts import render
from listings.models import Listing,Anouncement
from listings.choices import  prices_choices
from instructors.models import Instructor


# Create your views here.
def index(request):
    announcements = Anouncement.objects.order_by('-event_date')
    latest_listings = Listing.objects.order_by("-list_date").filter(is_published=True)[
        :3
    ]
    context = {
        "announcements":announcements,
        "listings": latest_listings,
        "prices_choices": prices_choices,

    }
    return render(request, "pages/index.html", context)


def about(request):
    intructor = Instructor.objects.all()
    best_seller = Instructor.objects.order_by("-id").filter(is_mvp=True)
    context = {
        "instructors": intructor,
        "best_seller": best_seller[0] if best_seller else "",
    }
    return render(request, "pages/about.html", context)
