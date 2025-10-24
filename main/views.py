from django.shortcuts import render

def main(request):
    return render(request, 'main/main.html')

def pro_nas(request):
    return render(request, 'main/pro_nas.html')

def kontakty(request):
    return render(request, 'main/kontakty.html')