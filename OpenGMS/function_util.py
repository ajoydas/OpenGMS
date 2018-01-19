from django.contrib.auth.decorators import user_passes_test
from django.template import loader
from django.http import Http404
from django.shortcuts import render


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        raise Http404
    return user_passes_test(in_groups)


def handler404(request):
    return render(request, 'template/404.html', status=404)