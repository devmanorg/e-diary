from itertools import groupby

from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from isoweek import Week

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject)


def get_iso_week_from_params(get_params):
    week_number = get_params.get('week', '')
    year_number = get_params.get('year', '')

    if week_number.isdigit() and year_number.isdigit():
        week_number = int(week_number)
        year_number = int(year_number)
        asked_iso_week = Week(year_number, week_number)
    else:
        # default weekday for that dvmn lesson
        current_iso_week = Week(2019, 1)
        asked_iso_week = current_iso_week
    return asked_iso_week


def format_day_title(date):
    day_formatter = '%A %d/%m/%Y'
    # Не стал прикручивать translate ради 7 переводов
    weekday_translations = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье',
    }
    formatted_day_title = date.strftime(day_formatter)
    for eng_titile, ru_title in weekday_translations.items():
        formatted_day_title = formatted_day_title.replace(eng_titile, ru_title)
    return formatted_day_title


def view_classes(request):
    classes = Schoolkid.objects.all().values_list(
        'year_of_study', 'group_letter').distinct()
    classes_groups = groupby(sorted(classes), key=lambda pair: pair[0])
    serialized_classes = {
        class_year: list(classes) for class_year, classes in classes_groups
    }
    unique_class_letters = sorted(set([letter for year, letter in classes]))
    context = {
        'unique_class_letters': unique_class_letters,
        'classes': serialized_classes
    }
    return render(request, 'classes.html', context)


def view_class_info(request, year, letter):
    schoolkids = get_list_or_404(
        Schoolkid, year_of_study=year, group_letter=letter)
    context = {
        'year': year,
        'letter': letter,
        'schoolkids': sorted(schoolkids, key=lambda kid: kid.full_name)
    }
    return render(request, 'class_info.html', context)


def view_schedule(request, year, letter):
    # по горизонтали время уроков,
    # по вертикали — название дней, в пересечении subject
    asked_iso_week = get_iso_week_from_params(request.GET)
    lessons_on_week = list(Lesson.objects.filter(
        year_of_study=year,
        group_letter=letter,
        date__week=asked_iso_week.week,
        date__year=asked_iso_week.year,
    ).order_by('date', 'timeslot'))
    if not lessons_on_week:
        raise Http404

    lessons_by_day = {}
    for day in asked_iso_week.days():
        formatted_day_title = format_day_title(day)
        lessons_by_day[formatted_day_title] = [
            lesson for lesson
            in lessons_on_week if lesson.date == day
        ]
    schedule = {}
    for formatted_day_title, lessons in lessons_by_day.items():
        that_day_schedule_blank = [None]*len(Lesson.TIMESLOTS_SCHEDULE)
        that_day_schedule = that_day_schedule_blank.copy()
        for lesson in lessons:
            that_day_schedule[lesson.timeslot - 1] = lesson
        if that_day_schedule == that_day_schedule_blank:
            that_day_schedule = []
        schedule[formatted_day_title] = that_day_schedule

    previous_week = asked_iso_week - 1
    next_week = asked_iso_week + 1
    context = {
        'class_year': year,
        'class_letter': letter,
        'next_week': next_week,
        'previous_week': previous_week,
        'schedule': schedule,
        'timeslots': Lesson.TIMESLOTS_SCHEDULE
    }
    return render(request, 'schedule.html', context)


def view_journal(request, year, letter, subject_id):
    # столбцы — дни, строки — ученики, пересечения — оценки
    asked_iso_week = get_iso_week_from_params(request.GET)
    subject = get_object_or_404(Subject, id=subject_id)
    schoolkids = Schoolkid.objects.filter(
        year_of_study=year, group_letter=letter).order_by('full_name')
    if not schoolkids:
        raise Http404
    marks_that_week = Mark.objects.filter(
        subject=subject,
        created__week=asked_iso_week.week,
        created__year=asked_iso_week.year,
    )

    all_marks = {}
    for schoolkid in schoolkids:
        schoolkid_marks = {}
        for day in asked_iso_week.days():
            schoolkid_day_marks = [
                mark for mark in marks_that_week
                if mark.created == day and mark.schoolkid == schoolkid
            ]
            formatted_day_title = format_day_title(day)
            schoolkid_marks[formatted_day_title] = schoolkid_day_marks
        all_marks[schoolkid] = schoolkid_marks

    previous_week = asked_iso_week - 1
    next_week = asked_iso_week + 1
    context = {
        'class_year': year,
        'class_letter': letter,
        'next_week': next_week,
        'previous_week': previous_week,
        'marks': all_marks,
        'subject': subject,
        'days': [format_day_title(day) for day in asked_iso_week.days()]
    }
    return render(request, 'journal.html', context)


def view_schoolkid(request, schoolkid_id):
    # успевамость по предметам, строки — предметы, столбцы — дни
    asked_iso_week = get_iso_week_from_params(request.GET)

    schoolkid = get_object_or_404(Schoolkid, id=schoolkid_id)
    subject_ids = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        date__week=asked_iso_week.week,
        date__year=asked_iso_week.year,
    ).values_list('subject__id')
    subjects = Subject.objects.filter(id__in=subject_ids)

    all_marks = {}
    for subject in subjects:
        subject_marks = {}
        marks_that_subject = Mark.objects.filter(
            subject=subject,
            schoolkid=schoolkid,
            created__week=asked_iso_week.week,
            created__year=asked_iso_week.year,
        )
        for day in asked_iso_week.days():
            that_day_that_subject_marks = [
                mark for mark in marks_that_subject if mark.created == day
            ]
            formatted_day_title = format_day_title(day)
            subject_marks[formatted_day_title] = that_day_that_subject_marks
        all_marks[subject] = subject_marks

    all_commendations = Commendation.objects.filter(
        schoolkid=schoolkid
    ).order_by('created')
    all_chastisements = Chastisement.objects.filter(
        schoolkid=schoolkid
    ).order_by('created')

    previous_week = asked_iso_week - 1
    next_week = asked_iso_week + 1
    context = {
        'next_week': next_week,
        'previous_week': previous_week,
        'schoolkid': schoolkid,
        'marks': all_marks,
        'all_commendations': all_commendations,
        'all_chastisements': all_chastisements,
        'days': [format_day_title(day) for day in asked_iso_week.days()]
    }
    return render(request, 'schoolkid_info.html', context)
