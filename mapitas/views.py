from django.shortcuts import render

# Create your views here.
def stats(request):
    return render(request, 'mapitas/index.html', {'request':request})
