from django.shortcuts import render
from django.core.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.http import *
from django.conf import settings
from django.contrib.gis import geos
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from h1n1.models import *
from datetime import datetime,timedelta
# from googlemaps import GoogleMaps
import random,string,ast

def home(request):
	''' Home page view of the django application'''
	return render_to_response('index.html')


def signup(request):
	"""signup for the user """
	if not request.user.is_active:
		if request.POST:
			print "entered the if sectison"
			username = request.POST['username']
			email = request.POST['email']
			password = request.POST['password']
			firstname = request.POST['firstname']
			lastname = request.POST['lastname']
			try:
				user = User.objects.create_user(username=username,email=email,password=password,first_name=firstname,last_name=lastname)
				user.save()
				return HttpResponseRedirect("/profile")
			except:
				return HttpResponse("This Id already exists")
		else:
			print "entered the else section"
			return render_to_response("register.html",context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/")	

def login(request):
	""" Login view """
	if not request.user.is_authenticated():
		if request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				# Correct password, and the user is marked "active"
				auth.login(request,user)
				# Redirect to a success page.
				return HttpResponseRedirect("/dashboard")
			else:
				# Show an error page
				return render_to_response('login.html',{'incorrect':1},context_instance=RequestContext(request))				
		return render_to_response('login.html',context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/dashboard")

# 	logout(request)
# 	# return HttpResponseRedirect("/")
# 	return render_to_response("index.html",{'logout':1},context_instance=RequestContext(request))

def dashboard(request):
	c = {}
	c.update(csrf(request))
	all_patients=PatientData.objects.filter(labId='1')
	return render_to_response('dashboard.html',{'all_patients':all_patients},context_instance=RequestContext(request))

def upload(request):
	# gmaps = GoogleMaps(api_key)
	# address = 'Constitution Ave NW & 10th St NW, Washington, DC'
	# lat, lng = gmaps.address_to_latlng(address)
	# print "###################",lat, lng
	c = {}
	c.update(csrf(request))
	return render_to_response('upload.html', context_instance=RequestContext(request))

def savelocation(request):
	c = {}
	c.update(csrf(request))
	if request.POST:
		print 'post request'
		name=request.POST['name']
		address=request.POST['address']
		latitude=request.POST['latitude']
		longitude=request.POST['longitude']
		print name,address,latitude,longitude
		point = "POINT(%s %s)" % (longitude, latitude)
		location = geos.fromstr(point)
		#patientId=''.join([random.choice(string.letters + string.digits) for i in range(10)])
		newpatient=PatientData(address=address,name=name,location=location,labId='1')
		newpatient.save()
		print 'patient details saved'
		return HttpResponseRedirect('/dashboard')
	return render_to_response('upload.html', context_instance=RequestContext(request))