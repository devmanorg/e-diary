from django.db import models


class Schoolkid(models.Model):
    full_name = models.CharField(max_length=200)
    birthday = models.DateField(null=True)
    year_started_education = models.IntegerField(null=True)
    year_of_study = models.IntegerField(null=True)
    year_of_study_group = models.CharField(max_length=1, null=True)

    def __str__(self):
        return f"{self.full_name} {self.year_of_study}{self.year_of_study_group}"


class Teacher(models.Model):
    full_name = models.CharField(max_length=200)
    birthday = models.DateField(blank=True, null=True)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    year_of_study = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.title} {self.year_of_study} класса"


class Lesson(models.Model):
    # title = models.CharField(max_length=200)
    year_of_study = models.IntegerField()
    year_of_study_group = models.CharField(max_length=1)
    timeslot = models.IntegerField()
    room = models.CharField(max_length=50)
    date = models.DateField()
    subject = models.ForeignKey(Subject, null=True)
    teacher = models.ForeignKey(Teacher, null=True)

    def __str__(self):
        return f"{self.subject.title} {self.year_of_study}{self.year_of_study_group}"


class Mark(models.Model):
    points = models.IntegerField()
    teacher_note = models.TextField(null=True)
    date = models.DateField()
    schoolkid = models.ForeignKey(Schoolkid)
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(Teacher)

    def __str__(self):
        return f"{self.points} {self.schoolkid.fullname}"


class Сhastisement(models.Model):
    text = models.TextField()
    date = models.DateField()
    schoolkid = models.ForeignKey(Schoolkid)
    subject = models.ForeignKey(Subject, null=True)
    teacher = models.ForeignKey(Teacher)

    def __str__(self):
        return f"{self.schoolkid.full_name}"


class Commendation(models.Model):
    text = models.TextField()
    date = models.DateField()
    schoolkid = models.ForeignKey(Schoolkid)
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(Teacher)

    def __str__(self):
        return f"{self.schoolkid.full_name}"
