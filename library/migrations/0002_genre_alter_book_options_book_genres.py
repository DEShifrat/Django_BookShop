# Generated by Django 4.1.2 on 2022-11-01 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название жанра')),
            ],
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title'], 'verbose_name': 'Книги', 'verbose_name_plural': 'Каталог книг'},
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(to='library.genre'),
        ),
    ]