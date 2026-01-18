from django.urls import path
from . import views

app_name = 'appointment_booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('about us/', views.about, name='about'),
    path('about/<int:id>/', views.about_doctor, name='about_doctor'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('doctors/',views.doctors,name='doctors'),
    path('appointment_booking/<int:id>/',views.book_appointment,name="get_appointment"),
    path('myappointment/',views.myappointment,name='myappointment'),
    path('doctordashboard/',views.viewdoctorappointment,name='doctordashboard'),
    path('profile/',views.profile,name='profile'),
    path("appointment/accept/<int:id>/", views.accept_appointment, name="accept_appointment"),
    path("appointment/reject/<int:id>/", views.reject_appointment, name="reject_appointment"),
    path("appointment/compleadtd/<int:id>/", views.complete_appointment, name="complete_appointment"),
    path("adddoctor/",views.add_doctor,name="add_doctor"),
    path("delete_doctor/<int:id>/",views.delete_doctor,name="delete_doctor"),
    path("doctor_list/",views.doctor_list,name="doctor_list")

]
