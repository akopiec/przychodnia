

from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForms, VisitForm, HomeForm, PrescriptionForm
from django.contrib.auth import authenticate, login
from .models import Visit, UserClinic, Prescription
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Uwierzytelnienie zakończylo się sukcesem')
                else:
                    messages.error(request, 'Konto jest zablokowane')
            else:
                messages.error(request, 'Nieprawidłowe dane ')
    else:
        form = LoginForm()
    return render(request, 'appl/login.html', {'form': form})


def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('/appl/login/')
    else:
        logout(request)


def register(request):
    if request.method == 'POST':
        user_form=UserRegistrationForms(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'appl/register_done.html', {'new_user': new_user})
    else:
        user_form=UserRegistrationForms()
    return render(request, 'appl/register.html', {'user_form': user_form})


@login_required
def add_visit(request):

    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            print("po valid")
            cd = form.cleaned_data
            doctor = cd['doctor']
            day = cd['day']
            hour_from = cd['hour_from']
            patient = cd['patient']
            valid_doctor = UserClinic.objects.get(username=doctor.username, role=1)
            valid_patient = UserClinic.objects.get(username=patient.username, role=2)
            valid_day_hour=len(Visit.objects.filter(doctor=valid_doctor, day=cd['day'], hour_from=cd['hour_from']))
            if valid_doctor is not None and valid_patient is not None and valid_day_hour == 0:
                visit = Visit(doctor=valid_doctor, patient=valid_patient, day=day, hour_from=hour_from)
                visit.save()
                messages.success(request, 'Wizyta została utworzona')
            else:
                if valid_doctor is None or valid_patient is None:
                    messages.info(request, 'Nie podano doktora lub pacjenta')
                else:
                    if valid_day_hour > 0:
                        messages.info(request, 'Wizyta w tym terminie jest zajęta')
    else:
        form = VisitForm()
    return render(request, 'appl/visit.html', {'form': form})


def home(request):
    if request.method == 'POST':
        home_form=HomeForm(request.POST)
        if home_form.is_valid():
            cd=home_form.cleaned_data
            doctor=cd['doctor_username']
            patient=cd['patient_username']
            if len(doctor) > 0 and len(patient) > 0:
                messages.error(request, 'podano zarówno dane pacjenta jak i doktora')
            else:
                if len(doctor) > 0:
                    try:
                        valid_doctor=UserClinic.objects.get(username=doctor,role=1)
                        visit_of_doctor=Visit.objects.filter(doctor=valid_doctor)

                        return render(request, 'appl/doctor_account.html',{'visit_of_doctor':visit_of_doctor,'doctor_username':doctor})
                    except ObjectDoesNotExist:
                        messages.error(request, "Wystapil problem za znalezieniem doktora")
                else:
                    if len(patient) > 0:
                        try:
                            valid_patient = UserClinic.objects.get(username=patient, role=2)
                            visit_of_patient = Visit.objects.filter(patient=valid_patient)
                            prescription = Prescription.objects.filter(patient=valid_patient)
                            prescriptions = prescription.order_by('doctor')
                            return render(request, 'appl/patient_account.html', {'visit_of_patient': visit_of_patient,'patient_username':patient,'prescription':prescriptions})
                        except ObjectDoesNotExist:
                            messages.error(request, 'wystąpił problem ze znalezieniem pacjenta')
    else:
        home_form = HomeForm()
    return render(request, 'appl/home.html', {'home_form': home_form})


def prescription(request,id):

    if request.method == 'POST':
        form_prescription = PrescriptionForm(request.POST)
        if form_prescription.is_valid():
            visit = Visit.objects.get(id=id)
            cd = form_prescription.cleaned_data
            medicines = cd['medicines']
            description = cd['description']
            prescription = Prescription(patient=visit.patient, doctor=visit.doctor, medicines=medicines, description=description)
            prescription.save()
            messages.success(request,'Dodano receptę')
            visit = Visit.objects.get(id=id)
            visit.delete()
            messages.success(request, 'Usunięto zapis z bazy pacjenta')
            return redirect('/appl/')
    else:
        form_prescription = PrescriptionForm()
    return render(request, 'appl/prescription.html', {'form_prescription': form_prescription})




