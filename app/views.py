from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import User
from .forms import UserForm


def _layout_context(**context):
    if settings.USE_DATABASE:
        context["user_count"] = User.objects.count()
    else:
        context["user_count"] = 0

    context["demo_mode"] = not settings.USE_DATABASE

    return context


def user_list(request):
    if not settings.USE_DATABASE:
        context = _layout_context(
            records=[],
            query="",
        )
        return render(request, "Listingpage.html", context)

    query = request.GET.get("q", "").strip()

    records = User.objects.all()

    if query:
        records = records.filter(Q(name__icontains=query) | Q(email__icontains=query))

    context = _layout_context(
        records=records,
        query=query,
    )

    return render(request, "Listingpage.html", context)


def demo_notice(request):
    return render(
        request,
        "Demo.html",
        {"demo_mode": True},
    )


def AddUser(request):
    if not settings.USE_DATABASE:
        return demo_notice(request)

    form = UserForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("/")

    context = _layout_context(form=form)

    return render(request, "Add.html", context)


def EditUser(request, id=None):
    if not settings.USE_DATABASE:
        return demo_notice(request)

    one_rec = User.objects.get(pk=id)

    form = UserForm(
        request.POST or None,
        request.FILES or None,
        instance=one_rec,
    )

    if form.is_valid():
        form.save()
        return redirect("/")

    context = _layout_context(form=form)

    return render(request, "Edit.html", context)


def DeleteUser(request, eid=None):
    if not settings.USE_DATABASE:
        return demo_notice(request)

    one_rec = User.objects.get(pk=eid)

    if request.method == "POST":
        one_rec.delete()
        return redirect("/")

    context = _layout_context()

    return render(request, "Delete.html", context)


def ViewUser(request, eid=None):
    if not settings.USE_DATABASE:
        return demo_notice(request)

    one_rec = User.objects.get(pk=eid)

    context = _layout_context(user=one_rec)

    return render(request, "View.html", context)
