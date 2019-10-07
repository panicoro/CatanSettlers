# Generated by Django 2.2.6 on 2019-10-07 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('BRICK', 'brick'), ('LUMBER', 'lumber'), ('WOOL', 'wool'), ('GRAIN', 'grain'), ('ORE', 'ore')], max_length=6)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
    ]
