# Generated by Django 4.0.4 on 2022-08-14 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techgridApp', '0003_accessable'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveys',
            name='img',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]