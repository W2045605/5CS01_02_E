from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.session')),
            ],
        ),
        migrations.CreateModel(
            name='UserCardProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[
                        ('not_started', 'Not Started'),
                        ('in_progress', 'In Progress'),
                        ('completed', 'Completed')
                    ],
                    default='not_started',
                    max_length=20
                )),
                ('vote', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.card')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'session', 'card')},
            },
        ),
    ]
