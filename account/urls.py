from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import include, re_path
from . import views
from django.urls import path



urlpatterns = [
    path('ajax/load_district/', views.load_district, name='load_district'),
    path('change_password/', views.change_password, name="change_password"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('index/', views.indexPage, name="index"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('info/', views.info, name="info"),
    path('', views.info2, name="info2"),
    path('add_College/', views.add_College, name="add_College"),
    path('Project/',views.Project, name="Project"),
    path('Guide/',views.Guide, name="Guide"),
    path('view_Guide/',views.view_Guide, name="view_Guide"),

    path('launch/',views.launch, name="launch"),
    path('curtain/',views.curtain, name="curtain"),

#path for guide view
    path('Guide_View/<str:pk>/',views.Guide_View, name="Guide_View"),
    path('view_Project/<str:pk>/',views.view_Project, name="view_Project"),
    path('total_survey/',views.total_survey, name="total_survey"),
    path('profile_update/',views.profile_update, name="profile_update"),
    path('view_survey/',views.view_survey, name="view_survey"),
    path('final_submit/<str:pk>/',views.final_submit, name="final_submit"),
    path('delete/<str:pk>/',views.delete, name="delete"),
    path('Reviewer/',views.Reviewer, name="Reviewer"),
    path('add_reviewer/',views.add_reviewer, name="add_reviewer"),
    path('reviewer_list/',views.reviewer_list, name="reviewer_list"),
    path('ajax/load_district/', views.load_district, name='load_district'),
    path('ajax/load_guide/', views.load_guide, name='load_guide'),
    path('Remarks/',views.Remarks, name="Remarks"),
    path('ViewRemarks/<str:pk>/',views.ViewRemarks, name="ViewRemarks"),
    path('updateRemarks/<str:pk>/',views.updateRemarks, name="updateRemarks"),
    path('AssignReviewer/<str:pk>/',views.AssignReviewer, name="AssignReviewer"),
    path('ReviewerRemarks/',views.ReviewerRemarks, name="ReviewerRemarks"),
    path('StudentGuide/',views.StudentGuide, name="StudentGuide"),
    path('StudentProject/',views.StudentProject, name="StudentProject"),
    # re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    # path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),
    path('college/', views.CollegeListView.as_view(),
         name='college-list'),
    path('college/<int:pk>', views.CollegeDetailView.as_view(),
         name='college-detail'),
    path('college/create', views.CollegeCreateView.as_view(),
         name='college-create'),
    path('college/<int:pk>/update', views.CollegeUpdateView.as_view(),
         name='college-update'),
    path('college/<int:pk>/delete', views.CollegeDeleteView.as_view(),
         name='college-delete'),


]

handler404 = 'account.views.handler404'
handler500 = 'account.views.handler500'