# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


from django.db import models
from django.conf import settings  # <-- vigtigt

# -------------------
# Patienter-app
# -------------------
class Patient(models.Model):
    cpr = models.CharField(max_length=11, unique=True)
    navn = models.CharField(max_length=100)
    kontakt = models.CharField(max_length=100, blank=True, null=True)
    paaroerende = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Patient"    # matcher din MySQL-tabel
        managed = False         # Django må ikke ændre tabellen

    def __str__(self):
        return f"{self.navn} ({self.cpr})"


class Encounter(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_tid = models.DateTimeField()
    slut_tid = models.DateTimeField(blank=True, null=True)
    afdeling = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Encounter"
        managed = False


class Notat(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    forfatter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    tid = models.DateTimeField()
    tekst = models.TextField()

    class Meta:
        db_table = "Notat"
        managed = False


class Diagnose(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    kode = models.CharField(max_length=20, blank=True, null=True)
    titel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "Diagnose"
        managed = False


class Allergi(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    stof = models.CharField(max_length=100)
    reaktion = models.CharField(max_length=255)
    alvorlighed = models.CharField(max_length=50)

    class Meta:
        db_table = "Allergi"
        managed = False


class Ordination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    laegemiddel = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "Ordination"
        managed = False


class Samtykke(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    formaal = models.CharField(max_length=255)
    gyldig_fra = models.DateField()
    gyldig_til = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "Samtykke"
        managed = False


class AuditEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    objekt_type = models.CharField(max_length=50)
    objekt_id = models.IntegerField()
    handling = models.CharField(max_length=50)
    tid = models.DateTimeField()

    class Meta:
        db_table = "AuditEvent"
        managed = False