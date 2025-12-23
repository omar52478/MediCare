from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("home/", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("my_availability/", views.my_availability_list, name="my_availability_list"),
    path("my_availability/add/", views.my_availability_add, name="my_availability_add"),
    path("my_availability/<int:availability_id>/delete/", views.my_availability_delete, name="my_availability_delete"),
    path("my_availability/<int:availability_id>/update/", views.my_availability_update, name="my_availability_update"),
    path("book/", views.book_appointment, name="book_appointment"),
    
    # Admin Dashboard URLs
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/patients/", views.admin_patients, name="admin_patients"),
    path("dashboard/doctors/", views.admin_doctors, name="admin_doctors"),
    path("dashboard/appointments/", views.admin_appointments, name="admin_appointments"),
    path("dashboard/specializations/", views.admin_specializations, name="admin_specializations"),
    path("dashboard/patient/<int:patient_id>/", views.admin_patient_detail, name="admin_patient_detail"),
    path("dashboard/doctor/<int:doctor_id>/", views.admin_doctor_detail, name="admin_doctor_detail"),
    path("dashboard/patient/<int:patient_id>/delete/", views.admin_patient_delete, name="admin_patient_delete"),
    path("dashboard/doctor/<int:doctor_id>/delete/", views.admin_doctor_delete, name="admin_doctor_delete"),
    path("dashboard/appointment/<int:appointment_id>/delete/", views.admin_appointment_delete, name="admin_appointment_delete"),
]

