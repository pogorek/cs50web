# Generated by Django 4.0.1 on 2022-02-01 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_listing_bid_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid_current',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
