from django.shortcuts import render

# Create your views here.
def index_view(req):
    context = {}
    return render(req, 'Index.html', context)