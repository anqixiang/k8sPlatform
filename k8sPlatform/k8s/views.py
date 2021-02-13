from django.shortcuts import render

# Create your views here.

def node(request):
    return render(request, 'k8s/node.html')