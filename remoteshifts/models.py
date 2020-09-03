from django.db import models

class LdapUser(models.Model):
    uid=models.SlugField(primary_key=True)
    supann_alias_login=models.CharField(max_length=16)
    mail=models.EmailField()
    given_name=models.CharField(max_length=128)
    sn=models.CharField(max_length=128)

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

class ScheduledRemoteShift(models.Model):
    user=models.ForeignKey(LdapUser, on_delete=models.CASCADE)
    day=models.DateField(verbose_name="Jour flottant de télétravail")

    class Meta:
        verbose_name = 'Jour flottant de télétravail'
        verbose_name_plural = 'Jours flottants de télétravail'
