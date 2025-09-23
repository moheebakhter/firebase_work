from http.client import responses

import requests
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
        convert_dict["id"] = a.id   # 👈 document ID bhi add kiya
        Contact.append(convert_dict)

    return render(request, "myapp/showdata.html", {"con": Contact})


def delete_contact(request, id):
    db.collection("contact").document(id).delete()
    return redirect("show")

def register(req):
    if req.method == "POST":
        n = req.POST.get("name")
        e = req.POST.get("email")
        p = req.POST.get("password")


        if not n or not e or not p:
            messages.error(req, "All Fields are required")
            return redirect("reg")

        if len(p) < 8:
            messages.error(req, "Password must be 8 characters long")
            return redirect("reg")
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_KEY}"
        playload = {
            "email" : e,
            "password" : p,
            "returnSecureToken": True

        }

        response = requests.post(url, playload)

        if response.status_code == 200:
            errorMsg= response.json()
            db.collection("User").add({
                "Name" : n,
                "Email" : e,
                "Pswd" : p,
                "Role" : "User",

            })

            messages.error(req, "User Registered Successfully")
            return redirect("reg")

    return render(req, "myapp/registration.html")

def Login(req):
    if req.method == "POST":
        e = req.POST.get("email")
        p = req.POST.get("password")

        if not e or not p:
            messages.error(req, "All Fields are Required")
            return redirect("log")

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_KEY}"
        playload = {
            "email" : e,
            "password" : p,
            "returnSecureToken" : True

        }
        res = requests.post(url,json=playload)

        if res.status_code == 200:
            userinfo = res.json()
            req.session["email"] = userinfo.get("email")
            return redirect("dashboard")
        else:
            error = res.json().get("error", {}).get("message", "Message Not Found")
            print(error)
            if error == "INVALID_LOGIN_CREDIENTIALS":
                messages.error(req, "Invalid credientials, Login Again")
            elif error == "INVALID_PASSWORD":
                messgaes.error(req, "Password is Incorrect")
            return redirect("log")
    return render(req, "myapp/login.html")

def dashboard(req):
    uemail = req.session["email"]
    return render(req, "myapp/dashboard.html", {"e" : uemail})


