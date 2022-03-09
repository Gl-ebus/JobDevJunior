from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import render
from django.db.models import Count
from DevJunior.models import Specialty, Company, Vacancy


class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all().annotate(count_vacancies=Count('vacancies'))
        specialties = Specialty.objects.all().annotate(count_vacancies=Count('vacancies'))
        context.update({
                    'specialties': specialties,
                    'companies': companies,
                      })
        return context


class AllVacancies(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


class VacanciesSpecialty(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context.update({
                'specialty': Specialty.objects.get(code=self.kwargs['spec']),
                'vacancies': Vacancy.objects.filter(specialty__code=self.kwargs['spec']),
            })

        except Specialty.DoesNotExist:
            raise Http404("Такой специализации у нас нет.")
        return context


class VacancyView(TemplateView):
    template_name = "DevJunior/vacancy.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['vacancy'] = Vacancy.objects.get(id=self.kwargs['id_vacancy'])
        except Vacancy.DoesNotExist:
            raise Http404("Извините, но вакансии, к которой вы пытаетесь получить доступ, не существует.")
        return context


class CompanyView(TemplateView):
    template_name = "company.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context.update({
                'company': Company.objects.get(id=kwargs.get("id_company")),
                'vacancies': Vacancy.objects.filter(company__id=kwargs.get("id_company")),
            })
        except Company.DoesNotExist:
            raise Http404("У данной компании нет вакансий.")
        return context


def custom_handler404(request, exception):
    return render(request, 'page404.html', context={'exception': exception})


def custom_handler500(request, *args, **argv):
    return render(request, 'page500.html', status=500)
