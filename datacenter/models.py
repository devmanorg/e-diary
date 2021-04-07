from django.db import models


class Schoolkid(models.Model):
    """Ученик."""
    full_name = models.CharField('ФИО', max_length=200)
    birthday = models.DateField('день рождения', null=True)

    entry_year = models.IntegerField('год начала обучения', null=True)
    year_of_study = models.IntegerField('год обучения', null=True)
    group_letter = models.CharField('литера класса', max_length=1, blank=True)

    def __str__(self):
        return f'{self.full_name} {self.year_of_study}{self.group_letter}'


class Teacher(models.Model):
    """Учитель."""
    full_name = models.CharField('ФИО', max_length=200)
    birthday = models.DateField('день рождения', null=True)

    def __str__(self):
        return f'{self.full_name}'


class Subject(models.Model):
    """Предмет: математика, русский язык и пр. — привязан к году обучения."""
    title = models.CharField('название', max_length=200)
    year_of_study = models.IntegerField(
        'год обучения', null=True, db_index=True,
    )

    def __str__(self):
        return f'{self.title} {self.year_of_study} класса'


class Lesson(models.Model):
    """Один урок в расписании занятий."""

    TIMESLOTS_SCHEDULE = [
        '8:00-8:40',
        '8:50-9:30',
        '9:40-10:20',
        '10:35-11:15',
        '11:25-12:05'
    ]

    year_of_study = models.IntegerField(db_index=True)
    group_letter = models.CharField(
        'литера класса', max_length=1, db_index=True,
    )

    subject = models.ForeignKey(
        Subject,
        null=True,
        verbose_name='предмет',
        on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher,
        null=True,
        verbose_name='учитель',
        on_delete=models.CASCADE)

    timeslot = models.IntegerField(
        'слот',
        db_index=True,
        help_text='Номер слота в расписании уроков на этот день.')
    room = models.CharField(
        'класс',
        db_index=True,
        max_length=50,
        help_text='Класс где проходят занятия.')
    date = models.DateField('дата', db_index=True)

    def __str__(self):
        return f'{self.subject.title} {self.year_of_study}{self.group_letter}'


class Mark(models.Model):
    """Оценка, поставленная учителем ученику."""
    points = models.IntegerField('оценка')
    teacher_note = models.TextField('комментарий', blank=True)
    created = models.DateField('дата')

    schoolkid = models.ForeignKey(
        Schoolkid,
        verbose_name='ученик',
        on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject,
        verbose_name='предмет',
        on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher,
        verbose_name='учитель',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.points} {self.schoolkid.full_name}'


class Chastisement(models.Model):
    """Запись с замечанием от учителя ученику."""
    text = models.TextField('замечание')
    created = models.DateField('дата', db_index=True)

    schoolkid = models.ForeignKey(
        Schoolkid,
        verbose_name='ученик',
        on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject,
        verbose_name='предмет',
        null=True,
        on_delete=models.SET_NULL)
    teacher = models.ForeignKey(
        Teacher,
        verbose_name='учитель',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.schoolkid.full_name}'


class Commendation(models.Model):
    """Запись с похвалой от учителя ученику."""
    text = models.TextField('похвала')
    created = models.DateField('дата', db_index=True)

    schoolkid = models.ForeignKey(
        Schoolkid,
        verbose_name='ученик',
        on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject,
        verbose_name='предмет',
        null=True,
        on_delete=models.SET_NULL)
    teacher = models.ForeignKey(
        Teacher,
        verbose_name='учитель',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.schoolkid.full_name}'
