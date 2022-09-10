from django.urls import path
from django.contrib import admin


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("admin/", admin.site.urls),
    path("add/", views.add, name='add'),
    path("logout/", views.logout_view, name="logout"),
    path("listings/<int:listing_id>", views.listing_details, name="listing_details"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close")
]
