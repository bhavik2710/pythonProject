from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from django.forms import ModelForm
from django.forms import Textarea
from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput, Select
from django.forms import SelectMultiple, TextInput, Select, DateInput, CheckboxSelectMultiple, RadioSelect, \
    CheckboxInput, Textarea

from .models import *
from .models import *
from django import forms
from captcha.fields import CaptchaField


class ChangepasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']


class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        widgets = {
            'address': Textarea(
                attrs={'class': 'form-control', 'rows': '2', 'cols': '50', 'placeholder': 'max length 500..'}),
            'Date_Of_Joining_Course': DateInput(attrs={'type': 'date'}),
            'Date_Of_Birth': DateInput(attrs={'type': 'date'}),
            'College_Name': Select(attrs={'style': 'width:100%', 'class': 'form-control select2'}),

            }


class Update_profile_Form(ModelForm):
    class Meta:
        model = Registration
        fields = ['First_name', 'Last_name', 'Date_Of_Birth', 'State', 'District', 'Gender', 'City', 'Address_Line1', 'Address_Line2', 'Pincode', 'Gender', 'Nationality', 'Role',
                  'Name_Of_Department', 'College_Name', 'Designation', 'Course_Details', 'Date_Of_Joining_Course', 'Course', 'Years', 'Correspondence_Sent_To', 'Last_Qualifying_Exam_Marksheet',
                  'Ncism_Teachers_Code', 'Alterner_Email_id', 'mobile', 'Telephone_No', 'Date_Of_Joining', ]
        exclude = ['Email_ID', 'User_ID', 'Full_Name', 'Type_Of_Faculty', 'is_reviewer', 'OTP_Verified', 'email_confirmed', 'Updated_On', ]
        widgets = {
            'address': Textarea(
                attrs={'class': 'form-control', 'rows': '2', 'cols': '50', 'placeholder': 'max length 500..'}),
            'Date_Of_Joining': DateInput(attrs={'type': 'date'}),
            'Date_Of_Joining_Course': DateInput(attrs={'type': 'date'}),
            'Date_Of_Birth': DateInput(attrs={'type': 'date'}),

            }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ChangepasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']


class CollegeForm(ModelForm):
    class Meta:
        model = College
        fields = '__all__'
        widgets = {

            }


class ProjectForm(ModelForm):
    class Meta:
        model = Project_info
        fields = '__all__'
        widgets = {

            'date': DateInput(attrs={'type': 'date'}),
            'Project_Title': Textarea(attrs={'class': 'form-control', 'rows': '2', 'cols': '50', 'placeholder': 'project title upto 25 words..'}),
            'Project_introduction': Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50', 'placeholder': 'introduction upto 300 words..'}),
            'Project_objective': Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '50', 'placeholder': 'objectives upto 100 words..'}),
            'Project_methodology': Textarea(attrs={'class': 'form-control', 'rows': '5', 'cols': '50', 'placeholder': 'methodology upto 800 words..'}),
            'Project_implication': Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '50', 'placeholder': 'implications upto 100 words..'}),
            'Project_reference': Textarea(attrs={'class': 'form-control', 'rows': '4', 'cols': '50', 'placeholder': 'references upto 300 words..'}),

            }


class GuideForm(ModelForm):
    class Meta:
        model = Guide_Info
        fields = '__all__'
        widgets = {

            'date': DateInput(attrs={'type': 'date'}),

            }


class ReviewerForm(ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        # fields = ['Marks','Remarks']
        widgets = {

            'date': DateInput(attrs={'type': 'date'}),

            }


class AssignReviewerForm(ModelForm):
    class Meta:
        model = Project_info
        fields = ['Reviewer_ID1', 'Reviewer_ID2', 'Reviewer_ID3']
        exclude = '__all__'


class MarksForm(ModelForm):
    class Meta:
        model = Project_info
        fields = ['Total_Marks', 'Remarks']
        exclude = '__all__'


class Review_MarksForm(ModelForm):
    class Meta:
        model = Review_Project_Score
        fields = '__all__'


class MyForm(forms.Form):
    captcha = CaptchaField()
