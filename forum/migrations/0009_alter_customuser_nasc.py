# Generated by Django 4.1.4 on 2022-12-27 16:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0008_alter_customuser_cidade_alter_customuser_estado_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="nasc",
            field=models.DateField(default=datetime.date(2022, 12, 27)),
        ),
    ]