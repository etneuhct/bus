# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from oauth2client import client
from django.shortcuts import redirect
from django.urls import reverse
import httplib2
from django.http import HttpResponse
from apiclient import discovery

# Create your views here.

class GoogleOauth(View):

    @staticmethod
    def get(request):
        client_secret_file = "client_secret.json"
        name = "BusFit"
        flow = client.flow_from_clientsecrets(filename=client_secret_file,
                                              scope=[
                                                  "https://www.googleapis.com/auth/plus.me",
                                                  "https://www.googleapis.com/auth/userinfo.email",
                                                  "https://www.googleapis.com/auth/userinfo.profile"]
                                              )
        flow.user_agent = name
        flow.params['include_granted_scopes'] = "true"
        flow.redirect_uri = "http://{}{}".format(request.META.get("HTTP_HOST"), reverse('google_oauth'))
        if "code" not in request.GET:
            auth_uri = flow.step1_get_authorize_url()
            return redirect(auth_uri)
        else:
            auth_uri = request.GET.get("code")
            credentials = flow.step2_exchange(auth_uri)
            request.session['credentials'] = credentials.to_json()
            return redirect(reverse('google_oauth_succeed'))

class GoogleOauthSucceed(View):
    @staticmethod
    def get(request):
        credentials = client.OAuth2Credentials.from_json(request.session["credentials"])
        http = httplib2.Http()
        http = credentials.authorize(http)
        people_service = discovery.build(serviceName='people', version='v1', http=http)
        people_resource = people_service.people()
        people_document = people_resource.get(resourceName="people/me", personFields="emailAddresses").execute()
        return HttpResponse("ok")

class GoogleOauthFailed(View):
    @staticmethod
    def get(request):
        return HttpResponse("fail")