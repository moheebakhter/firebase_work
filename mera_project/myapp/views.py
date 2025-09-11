from django.shortcuts import render, redirect
from django.contrib import messages
from mera_project.firebase_config import db


def contacts(request):
    if request.method == "POST":
        a = request.POST.get("name")
        b = request.POST.get("email")
        c = request.POST.get("subject")
        d = request.POST.get("message")

        db.collection("contact").add({
            "Name": a,
            "Email": b,
            "Subject": c,
            "Msg": d,
        })

        messages.success(request, "Query has been Submitted")
        return redirect("con")

    return render(request, "myapp/contact.html")


def Showdata(request):
    mydata = db.collection("contact").stream()
    Contact = []
    for a in mydata:
        convert_dict = a.to_dict()
        Contact.append(convert_dict)

    # yahan loop complete hone ke baad return
    return render(request, "myapp/showdata.html", {"con": Contact})
