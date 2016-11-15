# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 03:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_name', models.CharField(max_length=10)),
                ('current_high', models.IntegerField(default=0)),
                ('current_low', models.IntegerField(default=0)),
                ('general_trend', models.IntegerField(default=0)),
                ('start_date', models.DateField(verbose_name='Earliest Record')),
                ('end_date', models.DateField(verbose_name='Latest Record')),
            ],
        ),
        migrations.CreateModel(
            name='Stock_Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high', models.IntegerField(default=0)),
                ('low', models.IntegerField(default=0)),
                ('close', models.IntegerField(default=0)),
                ('open', models.IntegerField(default=0)),
                ('volume', models.IntegerField(default=0)),
                ('day', models.DateField(verbose_name='Day of Data')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predict_my_money.Stock')),
            ],
        ),
        migrations.CreateModel(
            name='Stock_Owned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bought_at', models.IntegerField(default=0)),
                ('bought_on', models.DateTimeField(verbose_name='date bought')),
                ('amount_owned', models.IntegerField(default=0)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predict_my_money.Stock')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_invested', models.IntegerField(default=0)),
                ('liquid_assets', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='stock_owned',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='predict_my_money.User'),
        ),
    ]
