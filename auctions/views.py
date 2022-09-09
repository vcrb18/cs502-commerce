from re import U
from tkinter.ttk import Widget
from turtle import title
from unicodedata import bidirectional
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django import forms
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Bid, User, Auction, Bids


# class WatchlistForm(forms.ModelForm):
#     user = forms.CharField()
#     item = forms.CharField()
#     # user = forms.CharField(widget=forms.HiddenInput())
#     # item = forms.CharField(widget=forms.HiddenInput())

#     class Meta:
#         model = Watchlist
#         fields = ['user', 'item']

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['price']

class ListingForm(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ['title', 'description', 'category', 'image', 'starting_bid']

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            #(Watchlist(user=user)).save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)
        if listing_form.is_valid():
            listing_form.save()
            messages.success(request, ('Your Listing was successfully added!'))
        else:
            messages.error(request, 'Error saving form')
        return HttpResponseRedirect(reverse("index"))
    listing_form = ListingForm()
    listings = Auction.objects.all()
    return render(request, "auctions/add.html", {
        'listing_form': listing_form,
        'listings': listings
    })


@login_required(login_url='auctions/login.html')
def listing_details(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "watchlist": watchlist
    })

@login_required(login_url='auctions/login.html')
def watchlist(request):
   watchlist = request.user.watchlist.all()
   return render(request, "auctions/watchlist.html", {
    "watchlist": watchlist
   })

@login_required(login_url='auctions/login.html')
def add_to_watchlist(request, listing_id):
    auction = get_object_or_404(Auction, id=listing_id)
    request.user.watchlist.add(auction)
    request.user.watchlist_counter += 1
    request.user.save()
    return HttpResponseRedirect(reverse('listing_details', args=(auction.id,)))

@login_required(login_url='auctions/login.html')
def remove_from_watchlist(request, listing_id):
    auction = get_object_or_404(Auction, id=listing_id)
    request.user.watchlist.remove(auction)
    request.user.watchlist_counter -= 1
    request.user.save()
    return HttpResponseRedirect(reverse('listing_details', args=(auction.id,)))

@login_required(login_url='auctions/login.html')
def bid(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.method == "POST":
        bid_price_form = BidForm(request.POST)
        if bid_price_form.is_valid():
            if bid_price_form > get_object_or_404(Bid, id=id).price:
                bid = get_object_or_404(Bid, id=id)
                bid.price, bid.user = bid_price_form, request.user
                bid.save()
                auction.save()
                return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('listing_details', args=(id,)))