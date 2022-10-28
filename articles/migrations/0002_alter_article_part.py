# Generated by Django 3.2.13 on 2022-10-28 14:15

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='part',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, '스트레칭'), (2, '윗가슴'), (3, '가슴중앙'), (4, '아랫가슴'), (5, '승모근'), (6, '광배근'), (7, '척추기립근'), (8, '전면삼각근'), (9, '후면삼각근'), (10, '측면삼각근'), (11, '이두근'), (12, '삼두근'), (13, '복근'), (14, '대퇴이두근'), (15, '대퇴사두근'), (16, '비복근')], max_length=38),
        ),
    ]
