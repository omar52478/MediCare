from django.contrib import admin
from .models import Profile, Doctor, DoctorAvailability, Specialization, Appointment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'age', 'national_id', 'governorate', 'city')
    search_fields = ('user__username', 'phone', 'national_id')
    list_filter = ('governorate', 'city')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__username', 'specialization__name')
    list_filter = ('specialization',)


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'start_time', 'end_time')
    search_fields = ('doctor__user__username',)
    list_filter = ('day', 'doctor')


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'day', 'time')
    search_fields = ('patient__username', 'doctor__user__username')
    list_filter = ('day', 'doctor')
