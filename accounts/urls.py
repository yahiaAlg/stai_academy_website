from django.urls import path
from . import views

# define your urlpatterns here
urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard_appendix", views.dashboard_appendix, name="dashboard_appendix"),
    path("announcements", views.announcements, name="announcements"),
    path("student_dashboard", views.student_dashboard, name="student_dashboard"),
    path("teacher_dashboard", views.teacher_dashboard, name="teacher_dashboard"),
    path("parent_dashboard", views.parent_dashboard, name="parent_dashboard"),
    path("notices", views.notices, name="notices"),
    path("notice/<int:notice_id>", views.notice, name="notice"),
    path("delete_notice", views.delete_notice, name="delete_notice"),
    path("update_notice", views.update_notice, name="update_notice"),
]
