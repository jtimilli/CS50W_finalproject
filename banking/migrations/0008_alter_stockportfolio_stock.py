# Generated by Django 4.1.5 on 2023-05-26 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0007_stockportfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockportfolio',
            name='stock',
            field=models.CharField(max_length=10),
        ),
    ]