from pprint import pprint
from django.contrib.auth.models import User
from .models import Designer, Profile, Student, Teacher


from django.db.models.signals import m2m_changed


def create_profile(sender, instance, action, **kwargs):
    if action == "post_add":
        affiliated_group = instance.groups.all().first()
        pprint(affiliated_group)
        match affiliated_group.name:
            case "teacher":
                Teacher.objects.create(owner=instance, role="teacher")
            case "student":
                Student.objects.create(owner=instance, role="student")
            case "parent":
                Profile.objects.create(owner=instance, role="parent")
            case "designer":
                Designer.objects.create(owner=instance, role="designer")
            case _:
                Profile.objects.create(owner=instance)
        print(f"profile was created for the user  {instance}")


m2m_changed.connect(create_profile, sender=User.groups.through)
