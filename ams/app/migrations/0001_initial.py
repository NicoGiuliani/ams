# Generated by Django 4.2 on 2023-05-09 19:01

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('common_name', models.CharField(max_length=50)),
                ('species', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=10)),
                ('date_acquired', models.DateField()),
                ('photo', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='images/')),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='FeedingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('food_type', models.CharField(blank=True, max_length=50, null=True)),
                ('food_quantity', models.IntegerField(blank=True, null=True)),
                ('last_fed_date', models.DateField(blank=True, null=True)),
                ('feed_interval', models.IntegerField(blank=True, null=True)),
                ('next_feed_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(blank=True, max_length=500, null=True)),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.entry')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='feeding_schedule',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.feedingschedule'),
        ),
    ]
