# Generated by Django 5.0.4 on 2024-05-19 12:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='receiver_transfers', to='account.profile')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sender_transfers', to='account.profile')),
            ],
        ),
    ]
