from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return f'{self.title}'


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.CharField(max_length=240)
    description = models.TextField()
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField()

    def __str__(self):
        return f'{self.title} в {self.company} (от {self.salary_min} до {self.salary_max} руб.)'
