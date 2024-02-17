from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLES = (
        ('student', 'student'),
        ('teacher', 'teacher'),
        ('designer', 'designer'),
        ('parent', 'parent')
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio =  models.TextField(max_length=500, blank=True)
    dp = models.ImageField(upload_to='dp/', default="default.jpg")
    role = models.CharField(max_length=8, choices=ROLES ,  default='student')
    def __str__(self) -> str:
        return f'Profile of {self.owner}'


class Departement(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    creation_date = models.DateTimeField(default=datetime.utcnow, blank=True)
    def __str__(self) -> str:
        return f'{self.name} (location: {self.location})'

class Subject(models.Model):
    SUBJECT_NAMES = (
        ("natural science", "natural science"),
        ("mathematics", "mathematics"),
        ("english language and literature", "English Language & Literature"),
        ("computer science", "Computer Science"),
    )
    name = models.CharField(max_length=32, choices=SUBJECT_NAMES)
    code = models.CharField(max_length=10)
    description = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.name


class Student(Profile):
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    subjects = models.ManyToManyField(Subject, related_name="students")
    def __str__(self) -> str:
        return f'student {super().__str__()}'

class Designer(Profile):
    class Meta:
        verbose_name = "Designer"
        verbose_name_plural = "Designers"

    affiliation_date = models.DateTimeField(default=datetime.utcnow)
    contract_duration = models.DurationField(blank=True, null=True)
    def __str__(self) -> str:
        return f'designer {super().__str__()}'


class Teacher(Profile):
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    subjects = models.ManyToManyField(Subject, related_name="teachers")
    department = models.ForeignKey(Departement, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"teacher {super().__str__()}"


class Anouncement(models.Model):
    designer_profile = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    anounce = models.ImageField(upload_to="anouncements/")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " by " + str(self.designer_profile)


class Notice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='notice', null=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, related_name="notice_sent", null=True
    )
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    date_sent = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'on {self.subject} about {self.title} by {self.teacher}'

class Gaurdianship(models.Model):
    parent = models.ForeignKey(Profile,related_name='parent',on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student,related_name='student',on_delete=models.SET_NULL, null=True)
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.parent} is guardian of {self.student}'
