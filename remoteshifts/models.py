from django.db import models

class LdapUser(models.Model):
    uid=models.SlugField(primary_key=True)
    supann_alias_login=models.CharField(max_length=16)
    mail=models.EmailField()
    given_name=models.CharField(max_length=128)
    sn=models.CharField(max_length=128)

    def __str__(self):
        return '%s %s' % (self.given_name, self.sn)

    class Meta:
        verbose_name = 'Utilisateur importé depuis le LDAP'
        verbose_name_plural = 'Utilisateurs importés depuis le LDAP'

class FixedRemoteShift(models.Model):
    user=models.ForeignKey(LdapUser, on_delete=models.CASCADE)
    DAY_CHOICES = [
        (1, 'Lundi'),
        (2, 'Mardi'),
        (3, 'Mercredi'),
        (4, 'Jeudi'),
        (5, 'Vendredi'),
    ]
    fixed_day=models.PositiveSmallIntegerField(
        choices=DAY_CHOICES,
        default=5,
        verbose_name="Jour fixe de télétravail",
        help_text = "Spécifier un jour fixe où vous serez en télétravail toutes les semaines"
    )

    class Meta:
        verbose_name = 'Jour fixe de télétravail'
        verbose_name_plural = 'Jours fixes de télétravail'

class PartTimeWorkDay(models.Model):
    user=models.ForeignKey(LdapUser, on_delete=models.CASCADE)
    DAY_CHOICES = [
        (1, 'Lundi'),
        (2, 'Mardi'),
        (3, 'Mercredi'),
        (4, 'Jeudi'),
        (5, 'Vendredi'),
    ]
    week_day=models.PositiveSmallIntegerField(
        choices=DAY_CHOICES,
        default=3,
        verbose_name="Jour de temps partiel",
        help_text = "Spécifier un jour où vous serez en temps partiel"
    )

    class Meta:
        verbose_name = 'Jour de temps partiel'
        verbose_name_plural = 'Jours de temps partiel'

class ScheduledRemoteShift(models.Model):
    user=models.ForeignKey(LdapUser, on_delete=models.CASCADE)
    day=models.DateField(verbose_name="Jour flottant de télétravail")

    class Meta:
        verbose_name = 'Jour flottant de télétravail'
        verbose_name_plural = 'Jours flottants de télétravail'

class ScheduledHalfDayOff(ScheduledRemoteShift):
    HALF_DAY_CHOICES = [
        ('am', 'Matin'),
        ('pm', 'Après-midi'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=HALF_DAY_CHOICES,
        default='pm',
    )

    class Meta:
        verbose_name = 'Demi-journée de congés'
        verbose_name_plural = 'Demi-journées de congés'
