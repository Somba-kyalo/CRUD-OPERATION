# app - views.py file

from django.db.models import Q
from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm

# Create your views here.


def _layout_context(**context):
    context["user_count"] = User.objects.count()
    return context


def user_list(request):
    query = request.GET.get("q", "").strip()
    records = User.objects.all()
    if query:
        records = records.filter(Q(name__icontains=query) | Q(email__icontains=query))
    mydict = _layout_context(records=records, query=query)
    return render(request, "Listingpage.html", context=mydict)


def AddUser(request):
    mydict = {}
    form = UserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("/")

    mydict = _layout_context(form=form)
    return render(request, "Add.html", mydict)


def EditUser(request, id=None):
    one_rec = User.objects.get(pk=id)
    form = UserForm(request.POST or None, request.FILES or None, instance=one_rec)
    if form.is_valid():
        form.save()
        return redirect("/")
    mydict = _layout_context(form=form)
    return render(request, "Edit.html", context=mydict)


def DeleteUser(request, eid=None):
    one_rec = User.objects.get(pk=eid)
    if request.method == "POST":
        one_rec.delete()
        return redirect("/")
    return render(request, "Delete.html", _layout_context())


def ViewUser(request, eid=None):
    one_rec = User.objects.get(pk=eid)
    return render(request, "View.html", _layout_context(user=one_rec))
