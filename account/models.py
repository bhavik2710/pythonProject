from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from uuid import uuid4
from django.contrib.sessions.models import Session
from django.conf import settings

# from multiselectfield import MultiSelectField

# create your model here.

# for state and district models here
class State_Study(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class District(models.Model):
    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Subject_Area(models.Model):
    Subject_Area = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Subject_Area


class Name_Of_Department(models.Model):
    Course = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Course


# For registration modelis here
class College(models.Model):
    # College_ID = models.PrimaryKey(User, null=True, blank=True, on_delete=models.CASCADE)

    # College_Name_Option = [('AIIMS', 'AIIMS'), ('JNU', 'JNU'), ('SBT', 'SBT'),('DU', 'DU'), ('IIT Delhi', 'IIT Delhi'), ('NIT Delhi', 'NIT Delhi') ]
    College_Name = models.CharField(max_length=500, blank=True, null=True)
    College_Address = models.CharField(max_length=100, blank=True, null=True)
    State = models.CharField(max_length=100, blank=True, null=True)
    City = models.CharField(max_length=100, blank=True, null=True)
    Pincode = models.CharField(max_length=100, blank=True, null=True)
    Phone_Number = models.CharField(max_length=100, blank=True, null=True)
    Updated_On = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    Remarks = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # return  str(self.State) + str(' --- ') + str(self.College_Name)
        return str(self.College_Name)

    class Meta:
        ordering = ('State',)


class Registration(models.Model):
    Title_option = [('Mr', 'Mr'), ('Miss', 'Miss'), ('Mrs', 'Mrs')]
    # Username = models.CharField(max_length=100, blank=True, null=True)
    Email_ID = models.CharField(max_length=100, blank=True, null=True)
    # Password = models.CharField(max_length=100, blank=True, null=True)
    # Re_Enter_Password = models.CharField(max_length=100, blank=True, null=True)
    First_name = models.CharField(max_length=100, null=True, validators=[MaxLengthValidator(100)])
    Last_name = models.CharField(max_length=100, null=True, validators=[MaxLengthValidator(100)])

    User_ID = models.OneToOneField(User, null=True, related_name='register_user', blank=True, on_delete=models.CASCADE)
    Date_Of_Birth = models.DateField(auto_now=False, null=True, auto_now_add=False, )
    Full_Name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    State = models.ForeignKey(State, null=True, on_delete=models.CASCADE,verbose_name="Student Residence State")
    District = models.ForeignKey(District, null=True, on_delete=models.CASCADE)

    City = models.CharField(max_length=100, null=True)
    Address_Line1 = models.CharField(max_length=500, null=True, validators=[MaxLengthValidator(500)])
    Address_Line2 = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    Pincode = models.CharField(max_length=100, blank=True, null=True)
    Name_Of_Department = models.CharField(max_length=200, blank=True, null=True, validators=[MaxLengthValidator(500)])
    # College_Name = models.CharField(max_length=100, blank=True, null=True)
    # College_Name_Option = [('AIIMS', 'AIIMS'), ('JNU', 'JNU'), ('SBT', 'SBT'),('DU', 'DU'), ('IIT Delhi', 'IIT Delhi'), ('NIT Delhi', 'NIT Delhi') ]
    College_Name = models.ForeignKey(College, null=True, blank=True, related_name='collegename',on_delete=models.CASCADE)
    Designation = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(200)])

    Gender_Option = [('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')]
    Gender = models.CharField(max_length=100, null=True, choices=Gender_Option)

    Nationality_Option = [('Indian', 'Indian'), ]
    Nationality = models.CharField(max_length=100, null=True, choices=Nationality_Option, default='Indian')
    Designation = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    Course_Details = models.CharField(max_length=200, blank=True, null=True, validators=[MaxLengthValidator(200)])
    Date_Of_Joining_Course = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )

    # Course_Option = [('BAMS', 'BAMS'), ('BioTechnology', 'BioTechnology'), ('BioInformatic', 'BioInformatic')]
    Course_Option = [('BAMS', 'BAMS')]
    Course = models.CharField(max_length=100, blank=True, null=True, choices=Course_Option)

    Years_Option = [('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th')]
    Years = models.CharField(max_length=100, blank=True, null=True, choices=Years_Option)

    Role_Option = [('Student', 'Student'), ('Guide', 'Guide'), ]
    Role = models.CharField(max_length=100, null=True, blank=True, choices=Role_Option)

    Correspondence_Sent_To_Option = [('Home', 'Home'), ('College', 'College'), ]
    Correspondence_Sent_To = models.CharField(max_length=100, blank=True, null=True, choices=Correspondence_Sent_To_Option)

    Last_Qualifying_Exam_Marksheet = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    Ncism_Teachers_Code = models.CharField(max_length=100, blank=True, null=True)
    is_reviewer = models.BooleanField(default=False)
    Alterner_Email_id = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    Telephone_No = models.CharField(max_length=100, blank=True, null=True)
    OTP_Verified = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    Date_Of_Joining = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    Type_Of_Faculty = models.CharField(max_length=100, blank=True, null=True)
    Updated_On = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    Student_study_state = models.ForeignKey(State_Study, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.First_name) + " " + str(self.Last_name) + "----" + str(self.College_Name)
        # return str(self.pk)


class Guide_Info(models.Model):
    User_ID = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # College_ID = models.PrimaryKey(User, null=True, blank=True, on_delete=models.CASCADE)
    Full_Name = models.CharField(max_length=100, blank=True, null=True)
    Designation = models.CharField(max_length=100, blank=True, null=True)
    Name_Of_Department = models.CharField(max_length=100, blank=True, null=True)
    Address_Line1 = models.CharField(max_length=100, blank=True, null=True)
    Address_Line2 = models.CharField(max_length=100, blank=True, null=True)
    College_Name = models.ForeignKey(College, null=True, blank=True, on_delete=models.CASCADE)

    # College_Name_Option = [('AIIMS', 'AIIMS'), ('JNU', 'JNU'), ('SBT', 'SBT'),('DU', 'DU'), ('IIT Delhi', 'IIT Delhi'), ('NIT Delhi', 'NIT Delhi') ]
    # College_Name = models.CharField(max_length=100, blank=True, null=True,choices=College_Name_Option)
    State = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
    District = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)

    City = models.CharField(max_length=100, blank=True, null=True)
    Pincode = models.CharField(max_length=100, blank=True, null=True)
    Mobile_Number = models.CharField(max_length=100, blank=True, null=True)
    Telephone_No = models.CharField(max_length=100, blank=True, null=True)
    # Nationality = models.CharField(max_length=100, blank=True, null=True)
    Nationality_Option = [('Indian', 'Indian'), ('Foreign', 'Foreign'), ]
    Nationality = models.CharField(max_length=100, blank=True, null=True, choices=Nationality_Option)
    # Gender = models.CharField(max_length=100, blank=True, null=True)
    Gender_Option = [('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')]
    Gender = models.CharField(max_length=100, blank=True, null=True, choices=Gender_Option)
    Email_id = models.CharField(max_length=100, blank=True, null=True)
    Updated_On = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    Remarks = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.Full_Name) + str(self.pk)


class Project_info(models.Model):
    # Spark_ID = models.PrimaryKey(User, null=True, blank=True, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    Guide_ID = models.OneToOneField(Registration, related_name="GUIDE_ID", null=True, on_delete=models.CASCADE, limit_choices_to={'Role': 'Guide',})
    Reviewer_ID1 = models.ForeignKey(Registration, related_name="Reviewer1_ID", null=True, blank=True, on_delete=models.CASCADE, limit_choices_to={'is_reviewer': True})
    Reviewer_ID2 = models.ForeignKey(Registration, related_name="Reviewer2_ID", null=True, blank=True, on_delete=models.CASCADE, limit_choices_to={'is_reviewer': True})
    Reviewer_ID3 = models.ForeignKey(Registration, related_name="Reviewer3_ID", null=True, blank=True, on_delete=models.CASCADE, limit_choices_to={'is_reviewer': True})
    Registration_ID = models.ForeignKey(Registration, related_name="Registration_ID", null=True, blank=True, on_delete=models.CASCADE)
    Application_Assertion_Form = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    Ethic_Communitee_Approval = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    Informed_Concent_Form = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    Case_Study_Form = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    Student_Questionnare = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    #Research_Proposal = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    Objective = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    Project_Title = models.CharField(max_length=200, null=True,verbose_name='Title',validators=[MaxLengthValidator(200)])
    Project_introduction = models.CharField(max_length=2100, null=True,blank=True, verbose_name='Introduction',validators=[MaxLengthValidator(2100)])
    Project_objective= models.CharField(max_length=700, null=True,blank=True,verbose_name='Objectives', validators=[MaxLengthValidator(700)])
    Project_methodology = models.CharField(max_length=5600, null=True,blank=True,verbose_name='Methodology', validators=[MaxLengthValidator(5600)])
    Project_implication= models.CharField(max_length=700, null=True,blank=True,verbose_name='Implications', validators=[MaxLengthValidator(700)])
    Project_reference = models.CharField(max_length=2100, null=True, blank=True,verbose_name='References',validators=[MaxLengthValidator(2100)])
    Type_Of_Study_Option = [('Literary Research', 'Literary Research'), ('Clinical Research', 'Clinical Research'),
                            ('Drug Research -  Medicinal Plant Research, Drug Standardization, Pharmacological Research', 'Drug Research -  Medicinal Plant Research, Drug Standardization, Pharmacological Research'), ]
    Type_Of_Study = models.CharField(max_length=100, null=True, choices=Type_Of_Study_Option)
    Subject_Area = models.ForeignKey(Subject_Area, null=True, on_delete=models.CASCADE)
    yes_no = [('Yes','Yes'),('No','No')]
    # Introduction = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    #
    # Methodology = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    # Implications = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    # References = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    Name_Of_Department = models.ForeignKey(Name_Of_Department, null=True, on_delete=models.CASCADE)
    Total_Marks = models.IntegerField(blank=True, null=True, default=0)
    final_submit = models.CharField(max_length=100, null=True, blank=True,default='No',choices=yes_no)
    Date_Created = models.DateField(auto_now_add=True, null=True, blank=True)
    Updated_On = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    Remarks = models.CharField(max_length=100, blank=True, null=True)
    College_Name = models.ForeignKey(College, null=True, blank=True, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=500, blank=True, null=True,
                                 validators=[MaxLengthValidator(100)])
    uniqueId = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4())
            super(Project_info, self).save(*args, **kwargs)
            self.unique_id = str('SPARK/') + str(self.Registration_ID.id) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(Project_info, self).save(*args, **kwargs)


class Review_Project_Score(models.Model):
    # Spark_ID = models.PrimaryKey(User, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    Reviewer = models.ForeignKey(Registration, related_name="Reviewer_ID", null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project_info, related_name="project_ID", null=True, blank=True, on_delete=models.CASCADE)
    Novelity = models.IntegerField(blank=True, null=True)
    Feasibility = models.IntegerField(blank=True, null=True)
    Candidate_Experience = models.IntegerField(blank=True, null=True)
    Relevence_To_Programme = models.IntegerField(blank=True, null=True)
    Guide_Experience = models.IntegerField(blank=True, null=True)
    Total_Marks_review = models.IntegerField(blank=True, null=True)
    Remarks = models.CharField(max_length=100, blank=True, null=True)
    Date_Created = models.DateField(auto_now_add=True, null=True, blank=True)
    Updated_On = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )

    def __str__(self):
        return str(self.pk)

    # class College_Name(models.Model):


## College_Name = models.CharField(max_length=100, blank=True, null=True,choices=College_Name_Option)


# class College_Name(models.Model):
# College_Name = models.CharField(max_length=100, blank=True, null=True)

# def __str__(self):
# S   return self.College_Name


class Course(models.Model):
    Course = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Course


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)