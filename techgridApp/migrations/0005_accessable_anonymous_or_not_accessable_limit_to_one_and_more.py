# Generated by Django 4.0.4 on 2022-09-06 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techgridApp', '0004_surveys_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessable',
            name='anonymous_or_not',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='accessable',
            name='limit_to_one',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='accessable',
            name='thankyou_message',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accessable',
            name='thankyou_or_not',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='accessable',
            name='allowedbyall',
            field=models.BooleanField(default=True),
        ),
    ]
