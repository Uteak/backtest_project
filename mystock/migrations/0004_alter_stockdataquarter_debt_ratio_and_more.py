# Generated by Django 4.1.5 on 2024-01-08 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystock', '0003_stockdata_rename_period_stockdataquarter_quarter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockdataquarter',
            name='debt_ratio',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdataquarter',
            name='dividend_propensity',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdataquarter',
            name='dividend_yield',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdataquarter',
            name='pbr',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdataquarter',
            name='per',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdataquarter',
            name='roe',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdatayear',
            name='debt_ratio',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdatayear',
            name='dividend_propensity',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdatayear',
            name='dividend_yield',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdatayear',
            name='pbr',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdatayear',
            name='per',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stockdatayear',
            name='roe',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
