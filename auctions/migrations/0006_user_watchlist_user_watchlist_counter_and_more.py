# Generated by Django 4.1 on 2022-08-26 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_watchlist_item_watchlist_items_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to='auctions.auction'),
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist_counter',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
