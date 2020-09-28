from django.shortcuts import render
from .models import Destination
import nsetools as nse
# Create your views here.
def index(request):

    text ='hiiiiiiiiiiiiii'
    return render(request, 'index.html', {'text':text})