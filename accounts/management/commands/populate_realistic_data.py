"""
Management command to populate the database with realistic Egyptian medical data.
Creates: 30 Doctors, 100 Patients, Real Specializations, Appointments & Availabilities
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, Doctor, Specialization, DoctorAvailability, Appointment
import random
from datetime import time

class Command(BaseCommand):
    help = 'Populates database with realistic Egyptian medical data'

    # Egyptian First Names
    MALE_NAMES = [
        'Ahmed', 'Mohamed', 'Mahmoud', 'Ali', 'Omar', 'Youssef', 'Khaled', 'Hassan',
        'Hussein', 'Ibrahim', 'Mostafa', 'Tarek', 'Amr', 'Karim', 'Sherif', 'Walid',
        'Hossam', 'Hazem', 'Ashraf', 'Samir', 'Nader', 'Fady', 'Ramy', 'Wael',
        'Ehab', 'Adel', 'Sayed', 'Ayman', 'Bassem', 'Magdy'
    ]
    
    FEMALE_NAMES = [
        'Fatma', 'Mona', 'Nour', 'Sara', 'Mariam', 'Aya', 'Dina', 'Heba',
        'Rania', 'Yasmin', 'Laila', 'Salma', 'Noha', 'Amira', 'Hana', 'Eman',
        'Sahar', 'Samira', 'Nagwa', 'Ghada'
    ]
    
    LAST_NAMES = [
        'ElSayed', 'Hassan', 'Ibrahim', 'Mohamed', 'Ahmed', 'Ali', 'Mahmoud',
        'Mostafa', 'Youssef', 'Khaled', 'Omar', 'Farouk', 'Nasser', 'Saleh',
        'Hamdy', 'Ramadan', 'Gaber', 'Rizk', 'Attia', 'Shehata', 'Soliman',
        'Ismail', 'Mansour', 'Zaki', 'Tawfik', 'Abdelrahman', 'Amer', 'Hussein'
    ]

    GOVERNORATES = [
        'Cairo', 'Alexandria', 'Giza', 'Shubra El Kheima', 'Port Said',
        'Suez', 'Luxor', 'Mansoura', 'Tanta', 'Asyut', 'Ismailia', 
        'Faiyum', 'Zagazig', 'Damietta', 'Aswan'
    ]

    CITIES = {
        'Cairo': ['Nasr City', 'Heliopolis', 'Maadi', 'Zamalek', 'Dokki', 'Mohandessin', 'New Cairo', 'October City'],
        'Alexandria': ['Smouha', 'Montazah', 'Miami', 'Stanley', 'San Stefano', 'Cleopatra'],
        'Giza': ['Dokki', 'Agouza', 'Faisal', 'Haram', 'Sheikh Zayed', '6th October'],
        'Shubra El Kheima': ['Shubra', 'El Qanater', 'Qalyub'],
        'Port Said': ['El Sharq', 'El Arab', 'Port Fouad'],
        'Suez': ['El Arbaeen', 'Faisal', 'Ataka'],
        'Luxor': ['Karnak', 'New Luxor', 'El Bayadieh'],
        'Mansoura': ['El Mahalla', 'Mit Ghamr', 'Dekernes'],
        'Tanta': ['El Mahalla El Kubra', 'Kafr El Zayat', 'Samanoud'],
        'Asyut': ['El Badari', 'Abnub', 'Manfalut'],
        'Ismailia': ['El Qantara', 'Fayed', 'Abu Sultan'],
        'Faiyum': ['Ibsheway', 'Tamiya', 'Etsa'],
        'Zagazig': ['Bilbeis', 'Abu Hammad', 'Minya El Qamh'],
        'Damietta': ['New Damietta', 'Kafr Saad', 'Faraskur'],
        'Aswan': ['Kom Ombo', 'Edfu', 'Daraw']
    }

    STREETS = [
        'El Tahrir Street', 'El Gomhoria Street', 'El Nasr Street', 'El Fath Street',
        'El Salam Street', 'El Nozha Street', 'El Borg Street', 'El Mahatta Street',
        'El Corniche', 'El Geish Street', 'El Sadat Street', 'El Azhar Street'
    ]

    RELATIONS = ['Father', 'Mother', 'Brother', 'Sister', 'Spouse', 'Son', 'Daughter', 'Uncle', 'Aunt']

    # Medical Specializations (Real Egyptian Hospital Departments)
    SPECIALIZATIONS = [
        ('Cardiology', 'Heart and cardiovascular system diseases, including heart attacks, heart failure, and arrhythmias'),
        ('Orthopedics', 'Bones, joints, ligaments, tendons, and muscles disorders and injuries'),
        ('Pediatrics', 'Medical care for infants, children, and adolescents'),
        ('Dermatology', 'Skin, hair, and nail conditions and diseases'),
        ('Ophthalmology', 'Eye diseases, surgeries, and vision care'),
        ('ENT', 'Ear, Nose, and Throat conditions and surgeries'),
        ('Neurology', 'Brain, spinal cord, and nervous system disorders'),
        ('Psychiatry', 'Mental health, emotional, and behavioral disorders'),
        ('Gastroenterology', 'Digestive system diseases including stomach, intestines, and liver'),
        ('Pulmonology', 'Lung and respiratory system diseases'),
        ('Nephrology', 'Kidney diseases and dialysis management'),
        ('Endocrinology', 'Hormonal disorders including diabetes and thyroid'),
        ('Oncology', 'Cancer diagnosis, treatment, and care'),
        ('Obstetrics & Gynecology', 'Women\'s reproductive health, pregnancy, and childbirth'),
        ('Urology', 'Urinary system and male reproductive system disorders'),
        ('Rheumatology', 'Arthritis, autoimmune diseases, and joint disorders'),
        ('General Surgery', 'Surgical treatment of various conditions'),
        ('Plastic Surgery', 'Reconstructive and cosmetic surgical procedures'),
        ('Dentistry', 'Teeth, gums, and oral health care'),
        ('Internal Medicine', 'General adult medicine and complex medical conditions'),
    ]

    DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

    def generate_phone(self):
        prefixes = ['010', '011', '012', '015']
        return f"{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

    def generate_national_id(self, age):
        birth_year = 2024 - age
        century = 2 if birth_year < 2000 else 3
        year = str(birth_year)[-2:]
        month = str(random.randint(1, 12)).zfill(2)
        day = str(random.randint(1, 28)).zfill(2)
        gov_code = str(random.randint(1, 35)).zfill(2)
        sequence = str(random.randint(1, 9999)).zfill(4)
        check = random.randint(1, 9)
        return f"{century}{year}{month}{day}{gov_code}{sequence}{check}"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🗑️  Clearing existing data...'))
        
        # Clear existing data
        Appointment.objects.all().delete()
        DoctorAvailability.objects.all().delete()
        Doctor.objects.all().delete()
        Profile.objects.all().delete()
        Specialization.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('✅ Existing data cleared!'))
        
        # Create Specializations
        self.stdout.write(self.style.WARNING('🏥 Creating specializations...'))
        specializations = []
        for name, desc in self.SPECIALIZATIONS:
            spec = Specialization.objects.create(name=name, description=desc)
            specializations.append(spec)
        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(specializations)} specializations!'))
        
        # Create 30 Doctors
        self.stdout.write(self.style.WARNING('👨‍⚕️ Creating 30 doctors...'))
        doctors = []
        doctor_titles = ['Prof. Dr.', 'Dr.', 'Dr.', 'Dr.', 'Consultant Dr.']
        
        for i in range(30):
            first_name = random.choice(self.MALE_NAMES if random.random() > 0.3 else self.FEMALE_NAMES)
            last_name = random.choice(self.LAST_NAMES)
            username = f"dr_{first_name.lower()}_{last_name.lower()}_{i+1}"
            email = f"{username}@hospital.eg"
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='doctor123',
                first_name=first_name,
                last_name=last_name,
                is_staff=True
            )
            
            doctor = Doctor.objects.create(
                user=user,
                specialization=random.choice(specializations)
            )
            doctors.append(doctor)
            
            # Create availability for each doctor (2-4 days)
            available_days = random.sample(self.DAYS, random.randint(2, 4))
            for day in available_days:
                start_hour = random.choice([8, 9, 10, 14, 15, 16])
                DoctorAvailability.objects.create(
                    doctor=doctor,
                    day=day,
                    start_time=time(start_hour, 0),
                    end_time=time(start_hour + random.randint(2, 4), 0)
                )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created 30 doctors with availabilities!'))
        
        # Create 100 Patients
        self.stdout.write(self.style.WARNING('🧑‍🤝‍🧑 Creating 100 patients...'))
        patients = []
        
        for i in range(100):
            is_male = random.random() > 0.45
            first_name = random.choice(self.MALE_NAMES if is_male else self.FEMALE_NAMES)
            last_name = random.choice(self.LAST_NAMES)
            username = f"patient_{first_name.lower()}_{i+1}"
            email = f"{username}@gmail.com"
            age = random.randint(18, 75)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='patient123',
                first_name=first_name,
                last_name=last_name
            )
            
            governorate = random.choice(self.GOVERNORATES)
            city = random.choice(self.CITIES.get(governorate, ['Downtown']))
            
            emergency_first = random.choice(self.MALE_NAMES + self.FEMALE_NAMES)
            emergency_last = random.choice(self.LAST_NAMES)
            
            profile = Profile.objects.create(
                user=user,
                phone=self.generate_phone(),
                age=age,
                national_id=self.generate_national_id(age),
                governorate=governorate,
                city=city,
                street=f"{random.randint(1, 150)} {random.choice(self.STREETS)}",
                emergency_name=f"{emergency_first} {emergency_last}",
                emergency_phone=self.generate_phone(),
                emergency_relation=random.choice(self.RELATIONS)
            )
            patients.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created 100 patients with profiles!'))
        
        # Create 150 Appointments
        self.stdout.write(self.style.WARNING('📅 Creating appointments...'))
        appointments_created = 0
        
        for _ in range(150):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            
            # Get doctor's availability
            availabilities = list(doctor.availabilities.all())
            if not availabilities:
                continue
            
            availability = random.choice(availabilities)
            
            # Check if appointment already exists
            exists = Appointment.objects.filter(
                patient=patient,
                doctor=doctor,
                day=availability.day,
                time=availability.start_time
            ).exists()
            
            if not exists:
                Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    day=availability.day,
                    time=availability.start_time
                )
                appointments_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created {appointments_created} appointments!'))
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('🎉 DATABASE POPULATED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'   📋 Specializations: {Specialization.objects.count()}')
        self.stdout.write(f'   👨‍⚕️ Doctors: {Doctor.objects.count()}')
        self.stdout.write(f'   🧑‍🤝‍🧑 Patients: {Profile.objects.count()}')
        self.stdout.write(f'   📅 Appointments: {Appointment.objects.count()}')
        self.stdout.write(f'   🕐 Availabilities: {DoctorAvailability.objects.count()}')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Login Credentials:'))
        self.stdout.write('   Doctors: password = "doctor123"')
        self.stdout.write('   Patients: password = "patient123"')
