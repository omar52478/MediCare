from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
import random

class Command(BaseCommand):
    help = 'Create 20 test users with profiles'

    def handle(self, *args, **kwargs):
        for i in range(1, 21):
            username = f"user{i}"

            user = User.objects.create_user(
                username=username,
                password="12345678",
                email=f"user{i}@test.com"
            )

            Profile.objects.create(
                user=user,
                phone=f"01000000{i:03}",
                age=random.randint(18, 60),
                national_id=f"1234567890{i:04}",
                governorate="Cairo",
                city="Nasr City",
                street=f"Street {i}",
                emergency_name=f"Emergency {i}",
                emergency_phone=f"01111111{i:03}",
                emergency_relation="Brother"
            )

        self.stdout.write(self.style.SUCCESS('✅ 20 users created successfully'))
