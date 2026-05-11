from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubmissionForm


def home(request):
    """Renders the homepage with hero section."""
    return render(request, 'activities/home.html')


def submit_choice(request):
    """Handles the activity choice submission form."""
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your choice has been submitted successfully!')
            return redirect('success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SubmissionForm()

    return render(request, 'activities/form.html', {'form': form})


def success(request):
    """Renders the elegant confirmation page."""
    return render(request, 'activities/success.html')
