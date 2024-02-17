from pprint import pprint
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


# Create your views here.
def register_v1(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:

            if User.objects.filter(username=username).exists():
                messages.error(request, f"this username: {username} is already taken!")
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"this email: {email} is already taken!")
                    return redirect("register")
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    # auth.login(request,user)
                    user.save()
                    messages.success(request, f"user {user} created successfully!")
                    return redirect("login")

        else:
            messages.error(request, "the passwords doesn't match")
            return redirect("register")
    return render(request, "accounts/register.html")


def login_v1(request):
    if request.method == "POST":
        username_given = request.POST.get("username", "")
        password_given = request.POST.get("password", "")
        print(f"the current user is:{username_given}")
        print(f"with password:{password_given}")
        user = auth.authenticate(
            request, username=username_given, password=password_given
        )
        if user is not None:
            print(f"user has been authenticated:")
            pprint(user)
            auth.login(request, user)
            messages.success(
                request, f"successfully logged in !\nWelcome back {username_given}"
            )
            return redirect("dashboard")
        else:
            messages.error(request, f"invalid credentials!")
            return redirect("login")
    return render(request, "accounts/login.html")


def logout_v1(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, f"you've logged-out successfully!")
        return redirect("dashboard")
    return redirect("dashboard")


def dashboard_v1(request):

    contacts = Contact.objects.order_by("-contact_date").filter(user=request.user)
    print("the retrieved contacts are:")
    pprint(contacts)
    context = {"contacts": contacts}
    return render(request, "accounts/dashboard.html", context)


from django.contrib.auth.models import Group
from pprint import pprint
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import *
from django.contrib import auth
from django.contrib import messages
from .forms import LoginUserForm, RegisterUserForm, AddNoticeForm
from .models import *


# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    contacts = Contact.objects.order_by("-contact_date").filter(user=request.user)
    print("the retrieved contacts are:")
    context = {"contacts": contacts}
    pprint(contacts)
    if request.user.groups.all().exists():

        user_group = str(request.user.groups.all().first().name)

        print(f"(shown in dashboard) {user_group} group is assigned to {request.user}")
        match user_group:
            case "student":
                return redirect("student_dashboard")
            case "parent":
                return redirect("parent_dashboard")
            case "teacher":
                return redirect("teacher_dashboard")
            case _:
                return render(request, "accounts/dashboard.html", context)
    else:
        return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
@is_allowed(allowed_roles=["student", "parent"])
def dashboard_appendix(request):
    contacts = Contact.objects.order_by("-contact_date").filter(user=request.user)
    print("the retrieved contacts are:")
    context = {"contacts": contacts}
    pprint(contacts)
    return render(request, "accounts/dashboard.html", context)


@unauthenticated_user
def register(request):

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(id=form.cleaned_data["group"]))
            pprint(user)

            # redirect to a success page.
            return redirect("dashboard")
        else:
            context = {"form": form}
            return render(request, "accounts/register.html", context)
    else:
        # If the request was GET, just render the form.
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, "accounts/register.html", context=context)


@unauthenticated_user
def login(request):

    if request.method == "POST":
        form = LoginUserForm(request.POST)
        username = form.data["username"]
        password = form.data["password1"]
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # The password matched correctly. Note that authenticate() does run the checks on whether this
            # user is active or not.
            auth.login(request, user)
            if request.user.groups.all().exists():
                user_group = str(request.user.groups.all().first().name)
                print(
                    f"(shown in login){user_group} group is assigned to {request.user}"
                )
                match user_group:
                    case "student":
                        return redirect("student_dashboard")
                    case "parent":
                        return redirect("parent_dashboard")
                    case "teacher":
                        return redirect("teacher_dashboard")
                    case _:
                        return render(request, "accounts/dashboard.html")
            else:
                return render(request, "accounts/dashboard.html")
        else:
            form = LoginUserForm()
            context = {"form": form}
            return render(request, "accounts/login.html", context)

    else:
        form = LoginUserForm()
        context = {"form": form}
        return render(request, "accounts/login.html", context)


def logout(request):
    auth.logout(request)
    return redirect("dashboard")


@login_required(login_url="login")
@is_allowed(allowed_roles=["designer"])
def announcements(request):
    """View for displaying all Announcements"""
    designer_profile = Designer.objects.get(owner=request.user)
    announcements = Anouncement.objects.filter(
        designer_profile=designer_profile
    ).order_by("-date_created")
    print("\nannouncements")
    pprint(announcements)
    context = {"announcements": announcements}
    return render(request, "accounts/announcements.html", context)


@is_allowed(allowed_roles=["student", "parent"])
def student_dashboard(request):
    if request.method == "POST":
        """View for Student Dashboard"""
        student_profile = Student.objects.get(
            owner=request.POST.get("user_student", "")
        )
    else:
        student_profile = Student.objects.get(owner=request.user)

    subjects = student_profile.subjects.all()
    notices = Notice.objects.filter(student=student_profile)
    context = {"notices": notices, "subjects": subjects}
    return render(request, "accounts/student_dashboard.html", context)

    # Handle the POST method here to add a new notice or remove a subject from the user's profile


@is_allowed(allowed_roles=["teacher"])
def teacher_dashboard(request):
    """View for Teacher Dashboard"""
    teacher_profile = Teacher.objects.get(owner=request.user)
    notices = Notice.objects.filter(teacher=teacher_profile)
    if request.method == "POST":
        print("currently adding...")
        form = AddNoticeForm(
            request.POST
        )


        if form.is_valid():
            notice = form.save()
            pprint(notice)  # Save the form (creates and saves a new Notice object)
            messages.success(request, "Successfully created notice!")
            return redirect("notice", notice.id)
        else:
            messages.error(request, f"{form.errors}")
            return redirect("teacher_dashboard")
    elif request.method == "GET":
        form = AddNoticeForm(
            initial={"teacher": Teacher.objects.get(owner=request.user)}
        )
    else:
        form = AddNoticeForm(
            initial={"teacher": Teacher.objects.get(owner=request.user)}
        )
        messages.warning(request, f"{request.method} method is not Allowed!")
    context = {"form": form, "notices": notices}
    return render(request, "accounts/teacher_dashboard.html", context)


@is_allowed(allowed_roles=["parent"])
def parent_dashboard(request):

    parent_profile = Profile.objects.filter(owner=request.user).first()
    related_students_gaurdianships = Gaurdianship.objects.filter(parent=parent_profile)
    # Get a list of students that are in the guardianship of this parent
    related_students = []
    for student_guardianship in related_students_gaurdianships:
        related_students.append(
            {
                "student_incheck": student_guardianship.student.owner,
                "notes_count": Notice.objects.filter(
                    student=student_guardianship.student
                )
                .distinct()
                .count(),
            }
        )

    context = {"related_students": related_students}

    return render(request, "accounts/parent_dashboard.html", context)


@login_required(login_url="login")
@is_allowed(allowed_roles=["student", "teacher"])
def notices(request):
    if request.user.groups.all().first().name == "teacher":
        teacher_profile = Teacher.objects.get(owner=request.user)
        notices = Notice.objects.filter(teacher=teacher_profile)
    elif request.user.groups.all().first().name == "student":
        student_profile = Student.objects.get(owner=request.user)
        notices = Notice.objects.filter(student=student_profile)
    context = {"notices": notices}
    return render(request, "accounts/notices.html", context)


@is_allowed(allowed_roles=["student", "parent", "teacher"])
def notice(request, notice_id):
    notice = Notice.objects.get(pk=notice_id)
    if request.user.groups.all().first().name in ["student", "parent"]:
        notice.is_read = True
    context = {"notice": notice}
    return render(request, "accounts/notice.html", context)


@login_required(login_url="login")
@is_allowed(allowed_roles=["teacher"])
def delete_notice(request):
    try:
        notice_pk = request.POST.get("notice_to_delete", "")
        if notice_pk:
            notice = Notice.objects.get(pk=notice_pk)
            notice.delete()
            messages.success(request, "Notice deleted successfully!")
        else:
            messages.warning(request, "No notice selected to delete.")
            redirect("notices")
    except Exception as e:
        print("Error while deleting the notice : ", e)
        messages.error(request, "An error occurred while deleting the notice.")

    return redirect("notices")


@login_required(login_url="login")
@is_allowed(allowed_roles=["teacher"])
def update_notice(request):
    if request.method == "POST":
        form = AddNoticeForm(request.POST)
        if form.is_valid():
            notice = form.save()
            messages.success(request, "The notice has been updated successfully.")
            redirect("notice", notice.id)
        else:
            messages.error(request, "the form is not a valid one!")
            return redirect("notices")
    elif request.method == "GET":
        print("currently updating")
        notice_id = request.GET.get("notice_to_edit", "")
        target_instance_notice = Notice.objects.get(pk=notice_id)
        pprint(target_instance_notice)
        form = AddNoticeForm(instance=target_instance_notice)
        pprint(form)
    else:
        messages.error(request, "not an allowed HTTP method")
        redirect("teacher_dashboard")
    context = {"form": form}
    return render(request, "accounts/teacher_dashboard.html", context)
