from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *


class DistrictAdmin(ImportExportModelAdmin):
    pass


class StateAdmin(ImportExportModelAdmin):
    pass


class CollegeAdmin(ImportExportModelAdmin):
    pass


class Subject_AreaAdmin(ImportExportModelAdmin):
    pass



class Registration1Admin(admin.ModelAdmin):
    list_display = ('id', 'First_name', 'User_ID', 'Designation', 'Role', 'is_reviewer')


class RegistrationAdmin(ImportExportModelAdmin,Registration1Admin):
    pass


class Project_infoAdmin1(admin.ModelAdmin):
    list_display = ('id', 'User_ID', 'Guide_ID', 'Reviewer_ID1', 'Reviewer_ID2', 'Reviewer_ID3','Registration_ID','unique_id')

class Project_infoAdmin(ImportExportModelAdmin,Project_infoAdmin1):
    pass


class Review_Project_ScoreAdmin(ImportExportModelAdmin):
    pass


class Name_Of_DepartmentAdmin(ImportExportModelAdmin):
    pass

class State_StudyAdmin(ImportExportModelAdmin):
    pass


# admin.site.register(State_Study, State_StudyAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Project_info, Project_infoAdmin)
admin.site.register(Guide_Info)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Course)
admin.site.register(Review_Project_Score, Review_Project_ScoreAdmin)
admin.site.register(Subject_Area, Subject_AreaAdmin)
admin.site.register(Name_Of_Department, Name_Of_DepartmentAdmin)
# admin.site.register(College_Name)
