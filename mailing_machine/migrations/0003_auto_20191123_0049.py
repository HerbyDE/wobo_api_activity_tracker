# Generated by Django 2.2.7 on 2019-11-23 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_machine', '0002_auto_20191122_0530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='woboconnection',
            name='admin_key',
        ),
        migrations.AlterField(
            model_name='woboconnection',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing_machine.WoBoCompany', verbose_name='Company'),
        ),
    ]