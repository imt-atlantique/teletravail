# Generated by Django 3.1.1 on 2020-09-04 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remoteshifts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledHalfDayOff',
            fields=[
                ('scheduledremoteshift_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='remoteshifts.scheduledremoteshift')),
                ('year_in_school', models.CharField(choices=[('am', 'Matin'), ('pm', 'Après-midi')], default='pm', max_length=2)),
            ],
            options={
                'verbose_name': 'Demi-journée de congés',
                'verbose_name_plural': 'Demi-journées de congés',
            },
            bases=('remoteshifts.scheduledremoteshift',),
        ),
        migrations.CreateModel(
            name='PartTimeWorkDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.PositiveSmallIntegerField(choices=[(1, 'Lundi'), (2, 'Mardi'), (3, 'Mercredi'), (4, 'Jeudi'), (5, 'Vendredi')], default=3, help_text='Spécifier un jour où vous serez en temps partiel', verbose_name='Jour de temps partiel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remoteshifts.ldapuser')),
            ],
            options={
                'verbose_name': 'Jour de temps partiel',
                'verbose_name_plural': 'Jours de temps partiel',
            },
        ),
    ]
