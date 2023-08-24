# Generated by Django 4.0.6 on 2023-08-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_alter_kcbmsuser_is_accountant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='school_type',
            field=models.CharField(choices=[('p', 'Primary School'), ('s', 'Secondary School'), ('t', 'Tertiary School')], default='p', max_length=100),
            preserve_default=False,
        ),
    ]
