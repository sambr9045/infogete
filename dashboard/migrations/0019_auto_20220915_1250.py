# Generated by Django 3.2.15 on 2022-09-15 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0018_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='transaction_type',
            field=models.CharField(default='newplan', max_length=200),
        ),
        migrations.CreateModel(
            name='partial_payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]