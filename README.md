#  Doctor Appointment Booking System

Django-based web application that allows users to book doctor appointments online.  
Different roles (Admin, Doctor, Patient) have role-specific access and features.

## 🚀 Features
- Role-based authentication (Admin | Doctor | Patient)
- Admin can add and manage doctors
- Patients can book and view appointments
- Doctors can view, accept, reject, and complete appointments
- Image upload for profile pictures
- Bootstrap-based responsive UI

## 📌 Technology Stack
- Django (Python)
- MySQL Database
- HTML, Bootstrap for UI

## 🧠 Models
### User
Custom user model extending AbstractUser with role field.

### Doctor
One-to-one field with User + profile info.

### Appointment
Foreign key to both User (patient) and Doctor.

## ▶️ How to Run Locally
1. Clone the repo  
   `git clone https://github.com/guru1889/Doctor-appointment.git`
2. Create and activate virtual environment  
   `python3 -m venv venv`  
   `source venv/bin/activate`
3. Install requirements  
   `pip install -r requirements.txt`
4. Create `.env` file for secrets
5. Migrate  
   `python manage.py migrate`
6. Run server  
   `python manage.py runserver`

## 🤝 Author
Guru – Backend Developer 
      
