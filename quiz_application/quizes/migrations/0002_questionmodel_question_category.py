# Generated by Django 4.2.14 on 2024-07-16 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionmodel',
            name='question_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quizes.quizcategories'),
            preserve_default=False,
        ),
    ]