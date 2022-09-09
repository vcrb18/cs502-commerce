from cProfile import label
from pickle import TRUE
from sre_parse import CATEGORIES
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = [
    ('SP', 'Sport'),
    ('Fd', 'Food'),
    ('T', 'Toys'),
    ('Off', 'Office'),
    ('CE', 'Computer and Electronics'),
    ('Fu', 'Furniture'),
    ('HPC', 'Health and Personal Care'),
    ('BMV', 'Books/Music/Video'),
    ('O', 'Other')
]

class Auction(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="static/auctions/media")
    starting_bid = models.IntegerField(null=True)
    price = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=3,
        choices=CATEGORIES
    )

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.starting_bid
        super(Auction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}: with a price of {self.price}"

class User(AbstractUser):
    watchlist_counter = models.IntegerField(default=0, blank=True)
    watchlist = models.ManyToManyField(Auction, related_name='watchlist', blank=True)

class Bid(models.Model):
    price = models.IntegerField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f"{self.price}"



class Comments(models.Model):
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"

# Many yo many comments


# class Watchlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
#     items = models.ManyToManyField(Auction, blank=True, related_name="watchlist_items")




