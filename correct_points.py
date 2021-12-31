from datacenter.models import Schoolkid
from datacenter.models import Mark


def correct_points():
    pupil = Schoolkid.objects.filter(full_name__contains="Фролов Иван")
    pupil = pupil[0]
    marks_query = Mark.objects.filter(schoolkid=pupil, points__lte=3)
    marks_total = marks_query.count()
    for index in range(marks_total):
        mark_to_correct = marks_query[index]
        mark_to_correct.points = 4
        mark_to_correct.save()

