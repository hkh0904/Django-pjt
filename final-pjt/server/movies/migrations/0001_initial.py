# Generated by Django 3.2 on 2023-05-24 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('adult', models.BooleanField(default=False)),
                ('backdrop_path', models.CharField(blank=True, max_length=100, null=True)),
                ('genre_ids', models.TextField(blank=True, max_length=100)),
                ('original_language', models.CharField(blank=True, max_length=20, null=True)),
                ('original_title', models.CharField(blank=True, max_length=100, null=True)),
                ('overview', models.CharField(blank=True, max_length=200, null=True)),
                ('popularity', models.FloatField(blank=True, null=True)),
                ('poster_path', models.CharField(blank=True, max_length=100, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('video', models.BooleanField(blank=True, null=True)),
                ('vote_average', models.FloatField(blank=True, null=True)),
                ('vote_count', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('username', models.CharField(max_length=20)),
                ('star', models.FloatField(default=0)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]
