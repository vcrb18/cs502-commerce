# Generated by Django 4.1 on 2022-09-10 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bids_auction_bids_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('auction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Bids',
        ),
    ]
