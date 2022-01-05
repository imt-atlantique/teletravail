from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator


import datetime
import csv

from .models import LdapUser, FixedRemoteShift, ScheduledRemoteShift, PartTimeWorkDay, ScheduledHalfDayOff

class IndexView(generic.ListView):
    model=LdapUser
    ordering = ['sn']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['now'] = now

        month = int(self.request.GET.get('month', now.month))

        if month >= 12:
            start = datetime.datetime(year=now.year,month=12, day=1)
            end = datetime.datetime(year=now.year,month=12, day=31)
        else:
            start = datetime.datetime(year=now.year,month=month, day=1)
            end = datetime.datetime(year=now.year,month=month+1, day=1)

        days=[]
        for i in range((end-start).days):
            days.append(datetime.datetime(year=start.year,month=start.month, day=1+i))

        context['days'] = days

        fixed_remote_shifts=FixedRemoteShift.objects.all()
        scheduled_remote_shifts=ScheduledRemoteShift.objects.filter(day__month=month)
        part_time_work_days=PartTimeWorkDay.objects.all()
        scheduled_half_days_off=ScheduledHalfDayOff.objects.filter(day__month=month)

        context['fixed_remote_shifts'] = fixed_remote_shifts
        context['scheduled_remote_shifts'] = scheduled_remote_shifts
        context['part_time_work_days'] = part_time_work_days
        context['scheduled_half_days_off'] = scheduled_half_days_off

        return context

def report_view(request, year, month):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teletravail_srcd.csv"'

    writer = csv.writer(response)
    writer.writerow(['Prénom', 'Nom', 'Email', 'Nombre de jours télétravaillés'])

    this_month = datetime.datetime(year=year,month=month, day=1)
    users = LdapUser.objects.all()
    
    day = datetime.datetime(year=year,month=month, day=1)
    week_days = [0, 0, 0, 0, 0]
    while day.month <= 1:
        if day.weekday() == 1:
            week_days[0]+=1
        elif day.weekday() == 2:
            week_days[1]+=1
        elif day.weekday() == 3:
            week_days[2]+=1
        elif day.weekday() == 4:
            week_days[3]+=1
        elif day.weekday() == 5:
            week_days[4]+=1
        day += datetime.timedelta(days=1)

    for user in users:
        scheduled_remote_shifts=ScheduledRemoteShift.objects.filter(user=user, day__month=month, day__year=year)
        fixed_remote_shifts=FixedRemoteShift.objects.filter(user=user)
        user_fixed_remote_shifts = 0
        if fixed_remote_shifts:
            for shift in fixed_remote_shifts:
                user_fixed_remote_shifts += week_days[shift.fixed_day-1]
        writer.writerow([user.given_name, user.sn, user.mail, len(scheduled_remote_shifts)+user_fixed_remote_shifts])

    return response

class UserDetailView(generic.DetailView):
    model = LdapUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        start = datetime.datetime(year=now.year,month=now.month, day=1)
        if now.month >= 12:
            start = datetime.datetime(year=now.year,month=12, day=1)
            end = datetime.datetime(year=now.year,month=12, day=31)
        else :
            start = datetime.datetime(year=now.year,month=now.month, day=1)
            end = datetime.datetime(year=now.year,month=now.month+1, day=1)

        days=[]
        for i in range((end-start).days):
            days.append(datetime.datetime(year=start.year,month=start.month, day=1+i))

        context['days'] = days

        fixed_remote_shifts=FixedRemoteShift.objects.filter(user=self.object)
        scheduled_remote_shifts=ScheduledRemoteShift.objects.filter(user=self.object)

        context['fixed_remote_shifts'] = fixed_remote_shifts
        context['scheduled_remote_shifts'] = scheduled_remote_shifts

        return context

class FixedRemoteShiftUpdateView(generic.UpdateView):
    model = FixedRemoteShift

@method_decorator(csrf_exempt, name='dispatch')
class FixedRemoteShiftCreateView(generic.CreateView):
    model = FixedRemoteShift
    fields = ['fixed_day']
    success_url = '/teletravail/'

    def form_valid(self, form):
        user = LdapUser.objects.get(pk=self.kwargs.get('uid'))
        form.instance.user = user
        return super().form_valid(form)

@method_decorator(csrf_exempt, name='dispatch')
class FixedRemoteShiftDeleteView(generic.DeleteView):
    model = FixedRemoteShift
    success_url = '/teletravail/'

@method_decorator(csrf_exempt, name='dispatch')
class ScheduledRemoteShiftUpdateView(generic.UpdateView):
    model = ScheduledRemoteShift

@method_decorator(csrf_exempt, name='dispatch')
class ScheduledRemoteShiftCreateView(generic.CreateView):
    model = ScheduledRemoteShift
    fields = ['day']
    success_url = '/teletravail/'

    def form_valid(self, form):
        user = LdapUser.objects.get(pk=self.kwargs.get('uid'))
        form.instance.user = user
        return super().form_valid(form)

@method_decorator(csrf_exempt, name='dispatch')
class ScheduledRemoteShiftDeleteView(generic.DeleteView):
    model = ScheduledRemoteShift
    success_url = '/teletravail/'
