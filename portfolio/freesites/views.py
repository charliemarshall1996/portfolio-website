from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InquiryForm
from .models import Inquiry

# Create your views here.


def is_superuser(user):
    return user.is_superuser


def home_view(request):
    return render(request, "freesites/index.html")


@login_required
@user_passes_test(is_superuser)  # Only superusers can access
def queue_list(request):
    # Filter out completed inquiries and order by their position (can use 'id' or 'created_at')
    inquiries = Inquiry.objects.filter(
        status__in=['pending', 'in_progress']).order_by('id')
    return render(request, 'freesites/queue_list.html', {'inquiries': inquiries})


@login_required
@user_passes_test(is_superuser)
def completed_list(request):
    # Filter out completed inquiries and order by their position (can use 'id' or 'created_at')
    inquiries = Inquiry.objects.filter(
        status='completed').order_by('id')
    return render(request, 'freesites/completed_list.html', {'inquiries': inquiries})


@login_required
@user_passes_test(is_superuser)
def complete_inquiry(request, inquiry_id):
    inquiry = Inquiry.objects.get(id=inquiry_id)
    inquiry.status = 'completed'
    inquiry.save()

    # Decrement the count of pending inquiries
    # This is an example, adjust logic as needed
    Inquiry.objects.filter(status='pending').update()

    return redirect('freesites:queue_list')


@login_required
@user_passes_test(is_superuser)
def in_progress_inquiry(request, inquiry_id):
    inquiry = Inquiry.objects.get(id=inquiry_id)
    inquiry.status = 'in progress'
    inquiry.save()
    return redirect('freesites:queue_list')


def queue_status(request, code):
    inquiry = get_object_or_404(Inquiry, code=code)
    position = inquiry.queue_position()
    return render(request, 'freesites/queue_status.html', {'inquiry': inquiry, 'position': position})


def queue_full(request):
    return render(request, 'freesites/queue_full.html')


def submit_inquiry(request):
    if Inquiry.objects.filter(status="pending").count() >= 10:
        return redirect('freesites:queue_full')  # Redirect to queue full page

    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            messages.success(
                request=request, message="Thank you for submitting your request. An email has been sent to you with a link to check your queue position.")

            queue_link = inquiry.get_queue_link()
            subject = "Your Website Inquiry Submission - Track Your Queue Position"
            message = f"Hello {inquiry.name},\n\nThank you for your inquiry. You can track your position in the queue here:\n{queue_link}\n\nWe'll update you as we progress!"
            send_mail(subject, message,
                      "charlie.marshall@charlie-marshall.dev", [inquiry.email])

            return redirect('freesites:queue', code=inquiry.code)
    else:
        form = InquiryForm()

    return render(request, 'freesites/submit_inquiry.html', {'form': form})
