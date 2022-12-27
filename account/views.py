from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.template import RequestContext
from django.views.generic.edit import UpdateView
from django.contrib.sessions.models import Session
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver

from .forms import *
from .tokens import account_activation_token


def indexPage(request):
    context = {}
    return render(request, 'index.html', context)


def launch(request):
    context = {}
    return render(request, 'inaugration.html', context)


def curtain(request):
    context = {}
    return render(request, 'curtain.html', context)


def loginPage(request):
    form = MyForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = MyForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('info')
            else:
                messages.info(request, 'Username OR password is incorrect')
        else:
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.info(request, 'Username OR password is incorrect')
            else:
                messages.info(request, 'incorrect Captcha')

    context = {'form': form}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def load_district(request):
    town = request.GET.get('district_id')
    continent = District.objects.filter(state=town).all()
    context = {'continent': continent}
    return render(request, 'district.html', context)


def load_guide(request):
    user = request.user
    register_college = Registration.objects.get(User_ID=request.user)
    college_id = register_college.College_Name
    # print(college_id)
    continent = Registration.objects.filter(College_Name=college_id, Role='Guide').values('id', 'First_name', 'Last_name', 'College_Name__College_Name', 'Name_Of_Department')
    print(continent)
    # college1 = College.objects.filter(id=college_id.id)
    # print(college1)
    # print(college_id.id__College_Name)
    context = {'continent': continent}
    return render(request, 'load_guide.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
        })


def info(request):
    # user = request.user
    # register = Registration.objects.get(User_ID=request.user)
    # role = register.Role
    # group1 = Group.objects.get(name=role)
    # group1.user_set.add(user)

    context = {}

    return render(request, 'info.html', context)


def info2(request):
    # user = request.user
    # register = Registration.objects.get(User_ID=request.user)
    # role = register.Role
    # group1 = Group.objects.get(name=role)
    # group1.user_set.add(user)
    if request.user.is_authenticated:
        return redirect('info')

    context = {}

    return render(request, 'info2.html', context)


@login_required(login_url='login')
def profile_update(request):
    try:
        register = Registration.objects.get(User_ID=request.user)
        userinfo = request.user
        form = Update_profile_Form(instance=register)
        if request.method == 'POST':
            form = Update_profile_Form(request.POST, instance=register, )
            if form.is_valid():
                form.save()
    except:
        register = None
        form = Update_profile_Form()

    context = {'register': register, 'form': form, }
    return render(request, 'profileupdate.html', context)


@login_required(login_url='login')
def add_College(request):
    form2 = CollegeForm()
    if request.method == 'POST':

        form2 = CollegeForm(request.POST)

        if form2.is_valid():
            form = form2.save()

            return redirect('login')

    context = {'form2': form2, }
    return render(request, 'College.html', context)


@login_required(login_url='login')
def Project(request):
    user = request.user
    register = Registration.objects.get(User_ID=request.user)
    form3 = ProjectForm()
    if request.method == 'POST':

        form3 = ProjectForm(request.POST, request.FILES)

        if form3.is_valid():
            auth1 = form3.save(commit=False)
            auth1.User_ID = user
            auth1.Registration_ID = register
            auth1.save()
            messages.success(request, 'Please fill the Assertion form and Refer scheme document for proposal format and  do the final submission by updating the relevant documents by clicking the final submit '
                                      'button')

            return HttpResponseRedirect(reverse(final_submit, args=(auth1,)))

        else:
            context = {'form3': form3, }
            return render(request, 'Project.html', context)

    context = {'form3': form3, }
    return render(request, 'Project.html', context)


@login_required(login_url='login')
## Reviewer
def Reviewer(request):
    form2 = ReviewerForm()
    if request.method == 'POST':

        form2 = ReviewerForm(request.POST)

        if form2.is_valid():
            form = form2.save()

            return redirect('info')

    context = {'form2': form2, }
    return render(request, 'Reviewer.html', context)


def registerPage(request):
    form1 = CreateUserForm()
    form2 = RegistrationForm()

    if request.method == 'POST':
        form1 = CreateUserForm(request.POST)
        form2 = RegistrationForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            form = form1.save(commit=False)
            # form.is_active = False
            form.save()
            username = form1.cleaned_data.get('username')

            auth1 = form2.save(commit=False)
            auth1.User_ID = form
            auth1.Email_ID = form.email
            auth1.save()
            email_user = form.email

            register = Registration.objects.get(User_ID=form)
            role = register.Role
            group1 = Group.objects.get(name=role)
            group1.user_set.add(form)
            current_site = get_current_site(request)
            # print(form.objects, 'oo')
            subject = 'Activate Your MySite Account'
            # message = render_to_string('account_activation_email.html', {
            #     'user': form,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(form.pk)),
            #     'token': account_activation_token.make_token(form),
            #     })
            # form.email_user(subject, message)

            message = render_to_string('account_activation_email.html', {
                'user': form,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(form.pk)),
                'token': account_activation_token.make_token(form),
                })
            # user.email_user(subject, message)
            send_mail(subject, message, 'no-reply-spark@bic.icmr.org.in', [email_user], )
            return redirect('account_activation_sent')
            # messages.success(request, 'Account was created for ' + username)
        else:
            context = {'form1': form1, 'form2': form2}
            return render(request, 'register.html', context)

    context = {'form1': form1, 'form2': form2}
    return render(request, 'register.html', context)


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user_obj = Registration.objects.get(User_ID=user.id)
        user.is_active = True
        # user.registration.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'account_activation_invalid.html')


### Guide View

@login_required(login_url='login')
def view_Guide(request):
    form4 = Guide_Info.objects.all()

    context = {'form4': form4}
    return render(request, 'view_Guide.html', context)


@login_required(login_url='login')
def Guide_View(request, pk):
    form3 = Project_info.objects.get(id=pk)

    context = {'form3': form3}
    return render(request, 'Guide_View.html', context)


#  Project view
@login_required(login_url='login')
def view_Project(request, pk):
    form3 = Project_info.objects.get(id=pk)

    context = {'form3': form3}
    return render(request, 'view_Project.html', context)


# - Total Survey--->
@login_required(login_url='login')
def total_survey(request):
    project = Project_info.objects.all()
    context = {'project': project}
    return render(request, 'total_survey.html', context)


# @login_required(login_url='login')


##Vieww survey
@login_required(login_url='login')
def view_survey(request):
    context = {}
    return render(request, 'view_survey.html', context)


## Update Survey

@login_required(login_url='login')
def final_submit(request, pk):
    user = request.user
    register = Registration.objects.get(User_ID=user)
    socio = Project_info.objects.get(id=pk)

    form3 = ProjectForm(instance=socio)
    if request.method == 'POST':
        form3 = ProjectForm(request.POST, request.FILES, instance=socio)
        if form3.is_valid():
            auth1 = form3.save(commit=False)
            auth1.User_ID = user
            auth1.Registration_ID = register
            auth1.final_submit = 'Yes'
            auth1.save()
            return redirect('StudentProject')
        else:
            context = {'form3': form3, 'socio': socio, }
            return render(request, 'update_survey.html', context)

    context = {'form3': form3, 'socio': socio, }
    return render(request, 'update_survey.html', context)


##Delete Survey

@login_required(login_url='login')
def delete(request, pk):
    socio = Project_info.objects.get(id=pk)

    if request.method == "POST":
        socio.delete()
        return redirect('total_survey')

    context = {'socio': socio}
    return render(request, 'delete.html', context)


#  Download concent form


def load_district(request):
    town = request.GET.get('district_id')
    continent = District.objects.filter(state=town).all()
    continent1 = District.objects.filter(state=town).all().count()
    print(continent1)
    context = {'continent': continent}
    return render(request, 'district.html', context)


# correction needed from here

# Reviewer View

@login_required(login_url='login')
def Remarks(request):
    form4 = Project_info.objects.filter(final_submit='Yes')

    context = {'form4': form4}
    return render(request, 'Remarks.html', context)


# View for view remarks

@login_required(login_url='login')
def ViewRemarks(request, pk):
    form3 = Project_info.objects.get(id=pk)
    form4 = Review_Project_Score.objects.filter(project=form3)
    context = {'form3': form3, 'form4': form4}
    return render(request, 'ViewRemarks.html', context)


# update remarks
@login_required(login_url='login')
def updateRemarks(request, pk):
    user = request.user
    register = Registration.objects.get(User_ID=request.user)
    project1 = Project_info.objects.get(id=pk)
    try:
        remarks = Review_Project_Score.objects.get(project=project1, Reviewer=register)
        if remarks is not None:
            return HttpResponse("<h2>Already been Reviewed</h2>")
    except:
        remarks = None
        print(remarks)
        marks = int(project1.Total_Marks)
        project = Review_MarksForm()
        if request.method == 'POST':
            project = Review_MarksForm(request.POST, request.FILES, )
            if project.is_valid():
                auth1 = project.save(commit=False)
                auth1.user = user
                auth1.Reviewer = register
                auth1.project = project1
                auth1.save()
                total_marks = int(auth1.Total_Marks_review)
                avg_marks = total_marks / 3
                print(avg_marks, 'avg_marks')
                update_marks = avg_marks + marks
                marks = Project_info.objects.filter(id=pk).update(Total_Marks=update_marks)
                return redirect('ReviewerRemarks')
            else:
                context = {'project': project, 'project1': project1}
                return render(request, 'updateRemarks.html', context)

    context = {'project': project, 'project1': project1}
    return render(request, 'updateRemarks.html', context)


@login_required(login_url='login')
def AssignReviewer(request, pk):
    project1 = Project_info.objects.get(id=pk)
    form5 = AssignReviewerForm(instance=project1)
    if request.method == 'POST':
        form5 = AssignReviewerForm(request.POST, request.FILES, instance=project1)
        if form5.is_valid():
            form5.save()
        return redirect('/Remarks')
    context = {'form5': form5, }
    return render(request, 'AssignReviewer.html', context)


# Views to  add marks

@login_required(login_url='login')
def Marks(request):
    form6 = Project_info.objects.all()

    context = {'form6': form6}
    return render(request, 'updateRemarks.html', context)


def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


@login_required(login_url='login')
def ReviewerRemarks(request):
    user = request.user
    try:
        register = Registration.objects.get(User_ID=user)
        form4 = Project_info.objects.filter(Q(Reviewer_ID1=register) | Q(Reviewer_ID2=register) | Q(Reviewer_ID3=register))
        form5 = Project_info.objects.filter(Q(Reviewer_ID1=register) | Q(Reviewer_ID2=register) | Q(Reviewer_ID3=register)).values('Reviewer_ID1', 'Reviewer_ID2', 'Reviewer_ID3', 'id')
        # print(form5, form5[0])
        rev1 = form5[0]['Reviewer_ID1']
        rev2 = form5[0]['Reviewer_ID2']
        rev3 = form5[0]['Reviewer_ID3']
        # print(rev1, rev2, rev3, )
        form6 = Project_info.objects.filter(Q(Reviewer_ID1=register) | Q(Reviewer_ID2=register) | Q(Reviewer_ID3=register)).prefetch_related('project_ID').all()
        # print(form6)
        form7 = Review_Project_Score.objects.filter(Reviewer=register)
    except:
        register = None
        form4 = None
        form5 = None
        form6 = None
        form7 = None
    # print(form7)
    context = {'form4': form4, 'form5': form5, 'form6': form6, 'form7': form7, }
    return render(request, 'ReviewerRemarks.html', context)


@login_required(login_url='login')
# Student Project
def StudentProject(request):
    try:
        user = request.user
        form3 = Project_info.objects.filter(User_ID=user)
    except:
        user = None
        form3 = None
    context = {'form3': form3}
    return render(request, 'StudentProject.html', context)


# Guide Project
@login_required(login_url='login')
def StudentGuide(request):
    user = request.user
    try:
        guide = Registration.objects.get(User_ID=user)
        form3 = Project_info.objects.filter(Guide_ID=guide)
    except:
        guide = None
        form3 = None
    context = {'form3': form3}
    return render(request, 'StudentGuide.html', context)


### Defining Roles for Student and Guide
@login_required(login_url='login')
def Guide(request):
    form4 = GuideForm()

    if request.method == 'POST':

        form4 = GuideForm(request.POST)

        if form4.is_valid():
            form = form4.save()

            return redirect('info')

    context = {'form4': form4, }
    return render(request, 'Guide.html', context)


@login_required(login_url='login')
def add_reviewer(request):
    form1 = CreateUserForm()
    form2 = RegistrationForm()
    if request.method == 'POST':
        form1 = CreateUserForm(request.POST)
        form2 = RegistrationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            form = form1.save(commit=False)
            form.is_active = False
            form.save()
            username = form1.cleaned_data.get('username')
            auth1 = form2.save(commit=False)
            auth1.User_ID = form
            auth1.Email_ID = form.email
            auth1.save()
            email_user = form.email

            register = Registration.objects.get(User_ID=form)
            role = register.Role
            group1 = Group.objects.get(name='Reviewer')
            group1.user_set.add(form)

            return redirect('reviewer_list')
            # messages.success(request, 'Account was created for ' + username)
        else:
            context = {'form1': form1, 'form2': form2}
            return render(request, 'add_reviewer.html', context)

    context = {'form1': form1, 'form2': form2}
    return render(request, 'add_reviewer.html', context)


@login_required(login_url='login')
def reviewer_list(request):
    register = Registration.objects.filter(is_reviewer=True)
    context = {'register': register, }
    return render(request, 'reviewer_list.html', context)


class CollegeListView(ListView):
    model = College
    template_name = 'college_list.html'
    context_object_name = 'books'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(CollegeListView, self).get_context_data(**kwargs)
        books = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(books, self.paginate_by)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        context['books'] = books
        return context


class CollegeDetailView(DetailView):
    model = College
    template_name = 'college_detail.html'
    context_object_name = 'book'


class CollegeUpdateView(UpdateView):
    model = College
    template_name = 'college_update.html'
    context_object_name = 'book'
    fields = ('College_Name', 'College_Address', 'State',)

    def get_success_url(self):
        return reverse('college-detail', kwargs={'pk': self.object.id})


class CollegeCreateView(CreateView):
    model = College
    template_name = 'college_create.html'
    fields = ('College_Name', 'College_Address', 'State',)
    success_url = reverse_lazy('college-list')


class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_delete.html'
    success_url = reverse_lazy('college-list')


def handler404(request, *args, **argv):
    response = render('404.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 500
    return response


@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    # remove other sessions
    Session.objects.filter(usersession__user=user).delete()

    request.session.save()

    UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key
        )
    return redirect('login')