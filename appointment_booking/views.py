from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group



#########permisions#

from django.http import HttpResponseForbidden
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "admin":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Admin access only")
    return wrapper

# Create your views here.
def home(request):
    doctors=Doctor.objects.all()
    return render(request,'home.html',{'doctors':doctors})
def about_doctor(request,id):
    doctor=Doctor.objects.get(id=id)
    return render(request,'about_doctor.html',{"doctor":doctor})


def about(request):
    return render(request,'about.html')
def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('appointment_booking:home')
            else:
                messages.error(request, "Invalid username or password")

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('appointment_booking:home')
    

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # ✅ CORRECT
            user.role = 'patient'
            user.save()
            #adding group
            paitent_group,created=Group.objects.get_or_create(name="paitent")
            user.groups.add(paitent_group)
            messages.success(request, "Register successful")
            return redirect('appointment_booking:login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
@permission_required('appointment_booking.add_appointment', raise_exception=True)
def doctors(request):
    doctors=Doctor.objects.all()
    return render(request,'doctors.html',{'doctors':doctors})


from django.http import HttpResponseForbidden

@login_required
@permission_required('appointment_booking.add_appointment', raise_exception=True)
def book_appointment(request, id):

    #  HARD BLOCK FOR DOCTOR
    if request.user.role == "doctor":
        return HttpResponseForbidden("Doctors cannot book appointments")

    doctor = Doctor.objects.get(id=id)

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date,
            time=time
        )

        messages.success(request, "Appointment booked successfully")
        return redirect('appointment_booking:myappointment')

    return render(request,'bookappointment.html',{'doctor':doctor})



@login_required
@permission_required('appointment_booking.view_appointment', raise_exception=True)
def myappointment(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'myappointment.html', {'appointments': appointments})


@login_required
@permission_required('appointment_booking.view_appointment', raise_exception=True)
def viewdoctorappointment(request):
    appointments=Appointment.objects.filter(doctor__user=request.user)


    print("Appointments count =", appointments.count())

    return render(request, "doctordashboard.html", {
        "appointments": appointments
    })
def profile(request):
    profile = request.user
    return render(request, "profile.html", {"profile": profile})


@login_required
@permission_required('appointment_booking.change_appointment', raise_exception=True)
def accept_appointment(request, id):
    appointment = get_object_or_404(
        Appointment,
        id=id,
        doctor__user=request.user   # doctor security check
    )
    appointment.status = "apppintment comfirm"
    appointment.save()
    return redirect("appointment_booking:doctordashboard")

@login_required
@permission_required('appointment_booking.change_appointment', raise_exception=True)
def reject_appointment(request, id):
    appointment = get_object_or_404(
        Appointment,
        id=id,
        doctor__user=request.user
    )
    appointment.status = "rejected"
    appointment.save()
    return redirect("appointment_booking:doctordashboard")


@login_required
@permission_required('appointment_booking.change_appointment', raise_exception=True)
def complete_appointment(request, id):
    appointment = get_object_or_404(
        Appointment,
        id=id,
        doctor__user=request.user
    )
    appointment.status = "compleated"
    appointment.save()
    return redirect("appointment_booking:doctordashboard")


@login_required
# @permission_required('appointment_booking.add_appointment', raise_exception=True)

@admin_required
def add_doctor(request):
    if request.method == "POST":

        username = request.POST["username"]

        #  CHECK duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Choose another.")
            return redirect("appointment_booking:add_doctor")

        # create doctor login user
        user = User.objects.create_user(
            username=username,
            password=request.POST["password"],
            role="doctor"
        )

        Doctor.objects.create(
            user=user,
            name=request.POST["name"],
            email=request.POST["email"],
            specialization=request.POST.get("specialization"),
            fees=request.POST.get("fees"),
            qualification=request.POST.get("qualification"),
            time=request.POST.get("time"),
            image=request.FILES.get("image")
        )
        doctors_group,created=Group.objects.get_or_create(name="doctors")
        user.groups.add(doctors_group)
        messages.success(request, "Doctor added successfully")
        return redirect("appointment_booking:doctor_list")

    return render(request, "admin/add_doctor.html")
# @admin_required
# def add_doctor(request):
#     if request.method == "POST":

#         print("POST RECEIVED")

#         username = request.POST["username"]
#         print("USERNAME:", username)

#         if User.objects.filter(username=username).exists():
#             print("USERNAME EXISTS")
#             messages.error(request, "Username already exists. Choose another.")
#             return redirect("appointment_booking:add_doctor")

#         user = User.objects.create_user(
#             username=username,
#             password=request.POST["password"],
#             role="doctor"
#         )

#         print("USER CREATED:", user.id)

#         doctor = Doctor.objects.create(
#             user=user,
#             name=request.POST["name"],
#             email=request.POST["email"],
#             specialization=request.POST.get("specialization"),
#             fees=request.POST.get("fees"),
#             qualification=request.POST.get("qualification"),
#             time=request.POST.get("time"),
#             image=request.FILES.get("image")
#         )

#         print("DOCTOR CREATED:", doctor.id)

#         return redirect("appointment_booking:doctor_list")

#     return render(request, "admin/add_doctor.html")




@admin_required
def doctor_list(request):
    doctors=Doctor.objects.all()
    return render(request,"admin/doctor_list.html",{"doctors":doctors})

@admin_required
def delete_doctor(request, id):
    doctor=get_object_or_404(Doctor,id=id)
    if doctor.user:
        doctor.user.delete()
    else:
        doctor.delete()
    return redirect("appointment_booking:doctor_list")


















    
    


