# Generated by Django 3.2.18 on 2023-02-14 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selectielijst', '0011_auto_20200807_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultaat',
            name='nummer',
            field=models.IntegerField(help_text='Nummer van het resultaat. Dit wordt samengesteld met het procestype en generiek resultaat indien van toepassing.', verbose_name='nummer'),
        ),
    ]
