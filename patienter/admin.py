from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from brugere.models import Bruger  # Importer Bruger fra den rigtige app
from .models import (
    Patient, Encounter, Notat, Diagnose,
    Allergi, Ordination, Samtykke, AuditEvent
)

# ===== Custom User Admin =====
class BrugerAdmin(BaseUserAdmin):
    list_display = ('brugernavn', 'navn', 'rolle', 'afdeling', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'rolle')
    fieldsets = (
        (None, {'fields': ('brugernavn', 'adgangskode')}),
        ('Personlige oplysninger', {'fields': ('navn', 'rolle', 'afdeling')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('brugernavn', 'navn', 'rolle', 'afdeling', 'adgangskode1', 'adgangskode2'),
        }),
    )
    search_fields = ('brugernavn', 'navn')
    ordering = ('brugernavn',)
    filter_horizontal = ('groups', 'user_permissions',)

# ===== Patient Admin =====
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('navn', 'cpr', 'kontakt', 'paaroerende')
    search_fields = ('navn', 'cpr', 'kontakt', 'paaroerende')

# ===== Encounter Admin =====
@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ('patient', 'start_tid', 'slut_tid', 'afdeling')
    list_filter = ('afdeling',)
    search_fields = ('patient__navn', 'patient__cpr')

# ===== Notat Admin =====
@admin.register(Notat)
class NotatAdmin(admin.ModelAdmin):
    list_display = ('encounter', 'forfatter', 'tid')
    search_fields = ('encounter__patient__navn', 'forfatter__navn', 'tekst')

# ===== Diagnose Admin =====
@admin.register(Diagnose)
class DiagnoseAdmin(admin.ModelAdmin):
    list_display = ('patient', 'kode', 'titel', 'status')
    search_fields = ('patient__navn', 'kode', 'titel', 'status')

# ===== Allergi Admin =====
@admin.register(Allergi)
class AllergiAdmin(admin.ModelAdmin):
    list_display = ('patient', 'stof', 'reaktion', 'alvorlighed')
    search_fields = ('patient__navn', 'stof', 'reaktion')

# ===== Ordination Admin =====
@admin.register(Ordination)
class OrdinationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'laegemiddel', 'dosis', 'status')
    search_fields = ('patient__navn', 'laegemiddel', 'status')

# ===== Samtykke Admin =====
@admin.register(Samtykke)
class SamtykkeAdmin(admin.ModelAdmin):
    list_display = ('patient', 'formaal', 'gyldig_fra', 'gyldig_til')
    search_fields = ('patient__navn', 'formaal')

# ===== AuditEvent Admin =====
@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'objekt_type', 'objekt_id', 'handling', 'tid')
    search_fields = ('user__navn', 'objekt_type', 'handling')
    list_filter = ('objekt_type', 'handling')
