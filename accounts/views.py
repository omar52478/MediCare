from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        
        # Validation: Check for empty fields
        if not username or not email or not password:
            return render(request, "signup.html", {
                "error": "Username, email, and password are required.",
                "form_data": request.POST
            })
        
        # Validation: Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "This username is already taken. Please choose a different one.",
                "form_data": request.POST
            })
        
        # Validation: Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {
                "error": "This email is already registered. Please use a different email or login.",
                "form_data": request.POST
            })
        
        # Validation: Check if national_id already exists
        national_id = request.POST.get("national_id", "").strip()
        if Profile.objects.filter(national_id=national_id).exists():
            return render(request, "signup.html", {
                "error": "This National ID is already registered.",
                "form_data": request.POST
            })
        
        # All validations passed - create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # create profile
        Profile.objects.create(
            user=user,
            phone=request.POST.get("phone", ""),
            age=request.POST.get("age", 0),
            national_id=national_id,
            governorate=request.POST.get("governorate", ""),
            city=request.POST.get("city", ""),
            street=request.POST.get("street", ""),
            emergency_name=request.POST.get("emergency_name", ""),
            emergency_phone=request.POST.get("emergency_phone", ""),
            emergency_relation=request.POST.get("emergency_relation", ""),
            image=request.FILES.get("image")
        )

        return redirect("login")

    return render(request, "signup.html")


from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")  
        else:
            error = "Invalid username or password"
            return render(request, "login.html", {"error": error})

    return render(request, "login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("login")


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Profile, Appointment, Doctor

@login_required
def profile_view(request):
    # أولاً: نشيك لو الـ User ده دكتور
    try:
        doctor = Doctor.objects.get(user=request.user)
        # لو دكتور، نوجهه لصفحة الدكتور
        return doctor_profile_view(request, doctor)
    except Doctor.DoesNotExist:
        pass
    
    # ثانياً: لو مش دكتور، يبقى مريض - نشيك على الـ Profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # لو Admin/Superuser وملوش profile
        if request.user.is_superuser:
            profile = Profile.objects.create(
                user=request.user,
                phone="N/A",
                age=0,
                national_id=f"ADMIN-{request.user.id}",
                governorate="N/A",
                city="N/A",
                street="N/A",
                emergency_name="N/A",
                emergency_phone="N/A",
                emergency_relation="N/A"
            )
        else:
            # مستخدم عادي وملوش profile
            return redirect("signup")
    
    # جيب مواعيد المريض
    patient_appointments = Appointment.objects.filter(patient=request.user).select_related('doctor__user', 'doctor__specialization')
    
    context = {
        "profile": profile,
        "patient_appointments": patient_appointments,
        "is_patient": True,
    }
    return render(request, "profile.html", context)


def doctor_profile_view(request, doctor):
    """صفحة Profile خاصة بالدكتور"""
    from .models import DoctorAvailability
    
    # مواعيد الدكتور (المرضى اللي حاجزين عنده)
    doctor_appointments = Appointment.objects.filter(doctor=doctor).select_related('patient')
    
    # أوقات الدكتور المتاحة
    availabilities = DoctorAvailability.objects.filter(doctor=doctor)
    
    context = {
        "doctor": doctor,
        "doctor_appointments": doctor_appointments,
        "availabilities": availabilities,
        "is_doctor": True,
    }
    return render(request, "doctor_profile.html", context)



@login_required
def home_view(request):
    # جلب الإحصائيات الحقيقية من قاعدة البيانات
    from django.contrib.auth.models import User
    
    context = {
        'doctor_count': Doctor.objects.count(),
        'specialization_count': Specialization.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'patient_count': Profile.objects.count(),  # عدد المرضى المسجلين
    }
    return render(request, "home.html", context)

def about_view(request):
    # Get real statistics from database
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Profile.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'specialization_count': Specialization.objects.count(),
    }
    return render(request, "about.html", context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Doctor, DoctorAvailability

@login_required
@user_passes_test(lambda u: u.is_staff, login_url="login")
def my_availability_add(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        # لو المستخدم staff بس مش دكتور
        return render(request, "error.html", {
            "error_title": "Not a Doctor",
            "error_message": "You need to be registered as a doctor to manage availability."
        })

    if request.method == "POST":
        day = request.POST["day"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        if start_time >= end_time:
            return render(request, "my_availability_form.html", {
                "doctor": doctor,
                "error": "End time must be after start time!"
            })
        DoctorAvailability.objects.create(
            doctor=doctor,
            day=day,
            start_time=start_time,
            end_time=end_time
        )
        return redirect("my_availability_list")

    return render(request, "my_availability_form.html", {"doctor": doctor})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url="login")
def my_availability_list(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        availabilities = doctor.availabilities.all()
    except Doctor.DoesNotExist:
        # لو المستخدم staff بس مش دكتور
        return render(request, "error.html", {
            "error_title": "Not a Doctor",
            "error_message": "You need to be registered as a doctor to manage availability."
        })
    return render(request, "my_availability_list.html", {"availabilities": availabilities})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url="login")
def my_availability_delete(request, availability_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    availability = get_object_or_404(DoctorAvailability, id=availability_id, doctor=doctor)
    availability.delete()
    return redirect("my_availability_list")



@login_required
@user_passes_test(lambda u: u.is_staff, login_url="login")
def my_availability_update(request, availability_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    availability = get_object_or_404(DoctorAvailability, id=availability_id, doctor=doctor)

    if request.method == "POST":
        day = request.POST["day"]
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]

        availability.day = day
        availability.start_time = start_time
        availability.end_time = end_time
        availability.save()

        return redirect("my_availability_list")

    return render(request, "my_availability_form_update.html", {"availability": availability})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Specialization, Doctor, DoctorAvailability, Appointment

@login_required
def book_appointment(request):
    specializations = Specialization.objects.all()

    spec_id = request.GET.get("specialization")
    doctor_id = request.GET.get("doctor")

    doctors = None
    availabilities = None

    if spec_id:
        doctors = Doctor.objects.filter(specialization_id=spec_id)

    if doctor_id:
        availabilities = DoctorAvailability.objects.filter(doctor_id=doctor_id)

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        slot = request.POST.get("slot")

        if doctor_id and slot:
            day, time_str = slot.split("|")

            # تحويل الوقت من string لـ datetime.time
            try:
                time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                messages.error(request, "Invalid time format.")
                return redirect(request.path + f"?specialization={spec_id}&doctor={doctor_id}")

            doctor = Doctor.objects.get(id=doctor_id)

            # الدكتور لا يحجز عند نفسه
            if doctor.user == request.user:
                messages.error(request, "You cannot book an appointment with yourself.")
                return redirect(request.path + f"?specialization={spec_id}&doctor={doctor_id}")

            # المريض لا يحجز نفس المعاد مرتين
            already_booked = Appointment.objects.filter(
                patient=request.user,
                day=day,
                time=time
            ).exists()

            if already_booked:
                messages.error(request, "You already have an appointment at this time.")
                return redirect(request.path + f"?specialization={spec_id}&doctor={doctor_id}")

            Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                day=day,
                time=time
            )

            messages.success(request, "Appointment booked successfully.")
            return redirect("profile")

    return render(request, "book.html", {
        "specializations": specializations,
        "doctors": doctors,
        "availabilities": availabilities,
        "selected_spec": int(spec_id) if spec_id else None,
        "selected_doctor": int(doctor_id) if doctor_id else None,
    })


# ============================================
# ADMIN DASHBOARD VIEWS
# ============================================

from django.db.models import Count
from django.core.paginator import Paginator

def admin_required(view_func):
    """Decorator to ensure only superusers can access admin views"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser:
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    """Main admin dashboard with overview statistics"""
    context = {
        'total_patients': Profile.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_specializations': Specialization.objects.count(),
        'recent_appointments': Appointment.objects.select_related('patient', 'doctor__user').order_by('-id')[:10],
        'recent_patients': Profile.objects.select_related('user').order_by('-id')[:10],
        'specialization_stats': Specialization.objects.annotate(doctor_count=Count('doctor')).order_by('-doctor_count')[:10],
        'doctors_by_spec': Doctor.objects.values('specialization__name').annotate(count=Count('id')).order_by('-count'),
    }
    return render(request, "admin/dashboard.html", context)


@admin_required  
def admin_patients(request):
    """List all patients with search and pagination"""
    search = request.GET.get('search', '')
    patients = Profile.objects.select_related('user').order_by('-id')
    
    if search:
        patients = patients.filter(
            user__username__icontains=search
        ) | patients.filter(
            user__email__icontains=search
        ) | patients.filter(
            phone__icontains=search
        ) | patients.filter(
            national_id__icontains=search
        )
    
    paginator = Paginator(patients, 20)
    page = request.GET.get('page', 1)
    patients = paginator.get_page(page)
    
    return render(request, "admin/patients.html", {
        'patients': patients,
        'search': search,
        'total_count': paginator.count
    })


@admin_required
def admin_doctors(request):
    """List all doctors with search and pagination"""
    search = request.GET.get('search', '')
    doctors = Doctor.objects.select_related('user', 'specialization').order_by('-id')
    
    if search:
        doctors = doctors.filter(
            user__username__icontains=search
        ) | doctors.filter(
            user__email__icontains=search
        ) | doctors.filter(
            specialization__name__icontains=search
        )
    
    paginator = Paginator(doctors, 20)
    page = request.GET.get('page', 1)
    doctors = paginator.get_page(page)
    
    return render(request, "admin/doctors.html", {
        'doctors': doctors,
        'search': search,
        'total_count': paginator.count
    })


@admin_required
def admin_appointments(request):
    """List all appointments with filtering"""
    search = request.GET.get('search', '')
    day_filter = request.GET.get('day', '')
    
    appointments = Appointment.objects.select_related('patient', 'doctor__user', 'doctor__specialization').order_by('-id')
    
    if search:
        appointments = appointments.filter(
            patient__username__icontains=search
        ) | appointments.filter(
            doctor__user__username__icontains=search
        )
    
    if day_filter:
        appointments = appointments.filter(day=day_filter)
    
    paginator = Paginator(appointments, 20)
    page = request.GET.get('page', 1)
    appointments = paginator.get_page(page)
    
    # Prepare days with selected state
    all_days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    days_with_state = [{'name': day, 'selected': day == day_filter} for day in all_days]
    
    return render(request, "admin/appointments.html", {
        'appointments': appointments,
        'search': search,
        'day_filter': day_filter,
        'total_count': paginator.count,
        'days': days_with_state
    })


@admin_required
def admin_specializations(request):
    """List all specializations with doctor counts"""
    specializations = Specialization.objects.annotate(
        doctor_count=Count('doctor'),
        appointment_count=Count('doctor__appointment')
    ).order_by('name')
    
    return render(request, "admin/specializations.html", {
        'specializations': specializations
    })


@admin_required
def admin_patient_detail(request, patient_id):
    """View detailed patient information"""
    profile = get_object_or_404(Profile, id=patient_id)
    appointments = Appointment.objects.filter(patient=profile.user).select_related('doctor__user', 'doctor__specialization')
    
    return render(request, "admin/patient_detail.html", {
        'profile': profile,
        'appointments': appointments
    })


@admin_required
def admin_doctor_detail(request, doctor_id):
    """View detailed doctor information"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availabilities = DoctorAvailability.objects.filter(doctor=doctor)
    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient')
    
    return render(request, "admin/doctor_detail.html", {
        'doctor': doctor,
        'availabilities': availabilities,
        'appointments': appointments
    })


@admin_required
def admin_patient_delete(request, patient_id):
    """Delete a patient"""
    profile = get_object_or_404(Profile, id=patient_id)
    username = profile.user.username
    profile.user.delete()  # This will cascade delete the profile too
    messages.success(request, f"Patient '{username}' has been deleted.")
    return redirect('admin_patients')


@admin_required
def admin_doctor_delete(request, doctor_id):
    """Delete a doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    username = doctor.user.username
    doctor.user.delete()  # This will cascade delete the doctor too
    messages.success(request, f"Doctor '{username}' has been deleted.")
    return redirect('admin_doctors')


@admin_required
def admin_appointment_delete(request, appointment_id):
    """Delete an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment has been deleted.")
    return redirect('admin_appointments')

