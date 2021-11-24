# Generated by Django 3.0.7 on 2021-11-24 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20211124_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubRubric',
            fields=[
            ],
            options={
                'verbose_name': 'Подрубрика',
                'verbose_name_plural': 'Подрубрики',
                'ordering': ('super_rubric__order', 'super_rubric__name', 'order', 'name'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.rubric',),
        ),
    ]