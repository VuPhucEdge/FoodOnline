from django.shortcuts import render


# vendor profile
def vprofile(request):
    return render(request, "vendor/vprofile.html")
