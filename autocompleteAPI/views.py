# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from authentication.models import Profile
from .serializer import UsernameSerializer


# Create your views here.


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def list(request):
    if request.method == 'GET':
        print("Getting Data in Rest Api.")
        print(request.GET.get('q'))
        profiles = Profile.objects.filter(user__username__icontains=request.GET.get('q'))\
            .filter(account_type=0)

        print(profiles)
        users = []
        for profile in profiles:
            users.append(profile.user)
        print(users)

        serializer = UsernameSerializer(users, many=True)
        serializer_data = serializer.data
        custom_data = {'results': serializer_data}

        print(JSONResponse(custom_data))
        return JSONResponse(custom_data)
