from django.shortcuts import render_to_response


def index(request):
		return render_to_response('bootstrap/index.html')


def about(request):
		return render_to_response('bootstrap/about.html')


def services(request):
		return render_to_response('bootstrap/services.html')


def contact(request):
		return render_to_response('bootstrap/contact.html')