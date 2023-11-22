from django import forms
from .models import UserClinic, Visit


class UserRegistrationForms(forms.ModelForm):
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label="powtórz hasło", widget=forms.PasswordInput)

    class Meta:
        model = UserClinic
        fields = ('username', 'city', 'street', 'house_number', 'role')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            print('Hasła są różne')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class VisitForm(forms.ModelForm):

    class Meta:
        model = Visit
        fields = ('doctor', 'patient', 'day', 'hour_from')


class HomeForm(forms.Form):
    doctor_username = forms.CharField(label="podaj nazwę doktora", required=False)
    patient_username = forms.CharField(label="podaj nazwę pacjenta", required=False)


class PrescriptionForm(forms.Form):
    medicines = forms.CharField(label="podaj przepisane leki", required=True)
    description = forms.CharField(label="opis przyjmowania leku", required=True)
