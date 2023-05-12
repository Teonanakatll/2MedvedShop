from django.shortcuts import render

from .forms import SubscriberForm


def landing(request):
    form = SubscriberForm(request.POST or None)

    # cleaned_data можно получить только после проверки is_valid()
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        data = form.cleaned_data
        print(data["name"])

        form.save()
    return render(request, 'landing/landing.html', locals())
