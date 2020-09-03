from django.views import generic
from django.utils import timezone

import datetime

from .models import LdapUser, FixedRemoteShift, ScheduledRemoteShift

class IndexView(generic.ListView):
    model=LdapUser
    ordering = ['sn']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['now'] = now

        month = int(self.request.GET.get('month', now.month))

        start = datetime.datetime(year=now.year,month=month, day=1)
        if month >= 12:
            end = datetime.datetime(year=now.year,month=month, day=31)
        else:
            end = datetime.datetime(year=now.year,month=month+1, day=31)

        days=[]
        for i in range((end-start).days):
            days.append(datetime.datetime(year=start.year,month=start.month, day=1+i))

        context['days'] = days

        fixed_remote_shifts=FixedRemoteShift.objects.all()
        scheduled_remote_shifts=ScheduledRemoteShift.objects.filter(day__month=month)

        context['fixed_remote_shifts'] = fixed_remote_shifts
        context['scheduled_remote_shifts'] = scheduled_remote_shifts

        return context

class UserDetailView(generic.DetailView):
    model = LdapUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        print(self)

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

class FixedRemoteShiftCreateView(generic.CreateView):
    model = FixedRemoteShift
    fields = ['fixed_day']
    success_url = '/teletravail/'

    def form_valid(self, form):
        user = LdapUser.objects.get(pk=self.kwargs.get('uid'))
        form.instance.user = user
        return super().form_valid(form)

class FixedRemoteShiftDeleteView(generic.DeleteView):
    model = FixedRemoteShift
    success_url = '/teletravail/'

class ScheduledRemoteShiftUpdateView(generic.UpdateView):
    model = ScheduledRemoteShift

class ScheduledRemoteShiftCreateView(generic.CreateView):
    model = ScheduledRemoteShift
    fields = ['day']
    success_url = '/teletravail/'

    def form_valid(self, form):
        user = LdapUser.objects.get(pk=self.kwargs.get('uid'))
        form.instance.user = user
        return super().form_valid(form)
