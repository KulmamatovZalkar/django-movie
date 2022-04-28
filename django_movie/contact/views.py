from django.views.generic import CreateView
# Create your views here.
from .models import Contact
from .forms import ContactForm

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "/"
