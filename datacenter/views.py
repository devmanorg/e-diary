from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Subject
from datacenter.models import Сhastisement
from django.shortcuts import render
from isoweek import Week


DAY_FORMATTER = '%A %d/%m/%Y'


def view_classes(request):
    classes = Schoolkid.objects.all().values_list(
        "year_of_study", "year_of_study_group").distinct()
    unique_class_groups = set([group for year, group in classes])
    unique_class_years = set([year for year, group in classes])
    serialized_classes = {
        unique_group: sorted([
            year for year, group
            in classes if group == unique_group
        ])
        for unique_group in sorted(list(unique_class_groups))
    }
    context = {
        "unique_class_years": unique_class_years,
        "classes": serialized_classes
    }
    return render(request, 'classes.html', context)


def view_class_info(request, year, letter):
    schoolkids_that_class = Schoolkid.objects.filter(
        year_of_study=year, year_of_study_group=letter)
    context = {
        "year": year,
        "letter": letter,
        "schoolkids": sorted(schoolkids_that_class, key=lambda kid: kid.full_name)
    }
    return render(request, 'class_info.html', context)


def view_schedule(request, year, letter):
    # по горизонтали время уроков, по вертикали — название дней, в пересечении subject
    iso_week_number = request.GET.get('week', None)
    iso_year_number = request.GET.get('year', None)

    if iso_week_number is None or iso_year_number is None:
        # current_iso_week = Week.thisweek()
        # default weekday for that dvmn lesson
        current_iso_week = Week(2019, 1)
        asked_iso_week = current_iso_week
    else:
        iso_week_number = int(iso_week_number)
        iso_year_number = int(iso_year_number)
        asked_iso_week = Week(iso_year_number, iso_week_number)
    iso_week_number = asked_iso_week.week
    iso_year_number = asked_iso_week.year
    asked_iso_week = Week(iso_year_number, iso_week_number)
    lessons_that_class = list(Lesson.objects.filter(
        year_of_study=year,
        year_of_study_group=letter,
        date__week=iso_week_number,
        date__year=iso_year_number,
    ))
    lesson_times = ["8:00-8:40", "8:50-9:30",
                    "9:40-10:20", "10:35-11:15", "11:25-12:05"]
    schedule = {}
    for day in asked_iso_week.days():
        lessons_that_day = [
            lesson for lesson
            in lessons_that_class if lesson.date == day
        ]
        that_day_schedule = {}
        for slot, lesson_time in enumerate(lesson_times, 1):
            lessons_that_time = [lesson for lesson in lessons_that_day
                                 if lesson.timeslot == slot]
            that_day_schedule[lesson_time] = lessons_that_time
        formatted_day_title = day.strftime(DAY_FORMATTER)
        schedule[formatted_day_title] = that_day_schedule
    previous_week = asked_iso_week - 1
    next_week = asked_iso_week + 1
    context = {
        "class_year": year,
        "class_letter": letter,
        "next_week_number": next_week.week,
        "previous_week_number": previous_week.week,
        "next_year_number": next_week.year,
        "previous_year_number": previous_week.year,
        "schedule": schedule,
        "timeslots": lesson_times
    }
    return render(request, 'schedule.html', context)


def view_journal(request, year, letter, subject_id):
    # столбцы — дни, строки — ученики, пересечения — оценки
    iso_week_number = request.GET.get('week', None)
    iso_year_number = request.GET.get('year', None)
    if iso_week_number is None or iso_year_number is None:
        # current_iso_week = Week.thisweek()
        # default weekday for that dvmn lesson
        current_iso_week = Week(2019, 1)
        asked_iso_week = current_iso_week
    else:
        iso_week_number = int(iso_week_number)
        iso_year_number = int(iso_year_number)
        asked_iso_week = Week(iso_year_number, iso_week_number)
    iso_week_number = asked_iso_week.week
    iso_year_number = asked_iso_week.year
    schoolkids_that_class = Schoolkid.objects.filter(
        year_of_study=year, year_of_study_group=letter).order_by("full_name")
    subject = Subject.objects.get(id=subject_id)
    marks_that_week = Mark.objects.filter(
        subject=subject, date__week=iso_week_number, date__year=iso_year_number)
    all_marks = {}
    for schoolkid in schoolkids_that_class:
        schoolkid_marks = {}
        for day in asked_iso_week.days():
            that_day_that_schoolkid_marks = [
                mark for mark in marks_that_week
                if mark.date == day and mark.schoolkid == schoolkid
            ]
            formatted_day_title = day.strftime(DAY_FORMATTER)
            schoolkid_marks[formatted_day_title] = that_day_that_schoolkid_marks
        all_marks[schoolkid] = schoolkid_marks
    previous_week = asked_iso_week - 1
    next_week = asked_iso_week + 1
    context = {
        "class_year": year,
        "class_letter": letter,
        "next_week_number": next_week.week,
        "previous_week_number": previous_week.week,
        "next_year_number": next_week.year,
        "previous_year_number": previous_week.year,
        "marks": all_marks,
        "subject": subject,
        "days": [day.strftime(DAY_FORMATTER) for day in asked_iso_week.days()]
    }
    return render(request, 'journal.html', context)


def view_schoolkid(request, schoolkid_id):
    # успевамость по предметам, строки — предметы, столбцы — дни
    iso_week_number = request.GET.get('week', None)
    iso_year_number = request.GET.get('year', None)
    if iso_week_number is None or iso_year_number is None:
        # current_iso_week = Week.thisweek()
        # default weekday for that dvmn lesson
        current_iso_week = Week(2019, 1)
        asked_iso_week = current_iso_week
    else:
        iso_week_number = int(iso_week_number)
        iso_year_number = int(iso_year_number)
        asked_iso_week = Week(iso_year_number, iso_week_number)
    iso_week_number = asked_iso_week.week
    iso_year_number = asked_iso_week.year
    schoolkid = Schoolkid.objects.get(id=schoolkid_id)
    subject_ids = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        year_of_study_group=schoolkid.year_of_study_group,
        date__week=iso_week_number,
        date__year=iso_year_number,
    ).values_list("subject__id")
    subjects = Subject.objects.filter(id__in=subject_ids)
    all_marks = {}
    for subject in subjects:
        subject_marks = {}
        marks_that_subject = Mark.objects.filter(
            subject=subject, schoolkid=schoolkid,
            date__week=iso_week_number, date__year=iso_year_number)
        for day in asked_iso_week.days():
            that_day_that_subject_marks = [mark for mark in marks_that_subject if mark.date == day]
            formatted_day_title = day.strftime(DAY_FORMATTER)
            subject_marks[formatted_day_title] = that_day_that_subject_marks
        all_marks[subject] = subject_marks
    all_commendations = Commendation.objects.filter(
        schoolkid=schoolkid
    ).order_by("date")
    all_chastisements = Сhastisement.objects.filter(
        schoolkid=schoolkid
    ).order_by("date")
    previous_week = asked_iso_week - 1
    next_week = asked_iso_week + 1
    context = {
        "next_week_number": next_week.week,
        "previous_week_number": previous_week.week,
        "next_year_number": next_week.year,
        "previous_year_number": previous_week.year,
        "class_year": schoolkid.year_of_study,
        "class_letter": schoolkid.year_of_study_group,
        "schoolkid": schoolkid,
        "marks": all_marks,
        "all_commendations": all_commendations,
        "all_chastisements": all_chastisements,
        "days": [day.strftime(DAY_FORMATTER) for day in asked_iso_week.days()]
    }
    return render(request, 'schoolkid_info.html', context)
