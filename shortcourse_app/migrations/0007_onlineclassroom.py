# Generated by Django 3.0.8 on 2020-10-14 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shortcourse_app', '0006_remove_students_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineClassRoom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=255)),
                ('room_pwd', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('session_years', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortcourse_app.SessionYearModel')),
                ('started_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortcourse_app.Instructors')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortcourse_app.Subjects')),
            ],
        ),
    ]