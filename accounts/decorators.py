from pprint import pprint
from django.shortcuts import  redirect, render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def user_redirector(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.all().exists():
            user_group = str(request.user.groups.all().first().name)
            print(f'{user_group} group is assigned to {request.user}')
            match user_group:
                case "student":
                    return redirect("student_dashboard")
                case  "parent":
                    return redirect("parent_dashboard")
                case  "teacher":
                    return redirect("teacher_dashboard")
                case _:
                    return view_func
        else:
            return render(request, "pages/index.html")
    return wrapper_func


def is_allowed(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                pprint(request.user.groups.all())
                group = request.user.groups.all().first()
                if group.name in allowed_roles:
                    return view_func(request, *args,**kwargs)
                else:
                    return redirect('index')
            else:
                return render(request, "pages/unauthorized.html")
        return wrapper_func        
    return decorator
