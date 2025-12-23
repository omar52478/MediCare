from accounts.models import Doctor


def user_role_context(request):
    """
    Context processor to add user role information to all templates.
    This allows templates to check if the current user is a doctor.
    """
    context = {
        'is_doctor': False,
        'is_patient': False,
    }
    
    if request.user.is_authenticated:
        # Check if user is a doctor
        context['is_doctor'] = Doctor.objects.filter(user=request.user).exists()
        # A patient is someone who is authenticated but not a doctor and not superuser
        context['is_patient'] = not context['is_doctor'] and not request.user.is_superuser
    
    return context
