# Generated by Django 4.1.5 on 2024-01-08 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockDataQuarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('period', models.CharField(max_length=15)),
                ('ROE', models.IntegerField(null=True)),
                ('PER', models.IntegerField(null=True)),
                ('PBR', models.IntegerField(null=True)),
                ('DebtRatio', models.IntegerField(null=True)),
                ('DividendYield', models.IntegerField(null=True)),
                ('DividendPropensity', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockDataYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('period', models.CharField(max_length=15)),
                ('ROE', models.IntegerField(null=True)),
                ('PER', models.IntegerField(null=True)),
                ('PBR', models.IntegerField(null=True)),
                ('DebtRatio', models.IntegerField(null=True)),
                ('DividendYield', models.IntegerField(null=True)),
                ('DividendPropensity', models.IntegerField(null=True)),
            ],
        ),
    ]
