from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Announcement


@login_required
def home(request):
    announcements = Announcement.objects.all().order_by('date')
    return render(request, 'home.html', {'announcements': announcements})
