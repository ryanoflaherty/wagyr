from django.shortcuts import render_to_response, render
from app.forms import dailySchedForm

def index(request):
		return render_to_response('bootstrap/index.html')


def about(request):
		return render_to_response('bootstrap/about.html')


def services(request):
		return render_to_response('bootstrap/services.html')


def contact(request):
		return render_to_response('bootstrap/contact.html')


def daily_sched(request):
	if request.method == 'POST':
		form = dailySchedForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)

			# Now call the index() view.
			# The user will be shown the homepage.
			return index(request)

	else:
		# If the request was not a POST, display the form to enter details.
		form = dailySchedForm()

		# Bad form (or form details), no form supplied...
		# Render the form with error messages (if any).
		return render(request, 'bootstrap/daily_sched.html', {'form': form})