# Generated by Django 5.0.1 on 2024-02-21 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HelloBlog', '0002_rename_imagem_publicacao_thumnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicacao',
            old_name='thumnail',
            new_name='thumbnail',
        ),
    ]
