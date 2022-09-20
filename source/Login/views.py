from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import redirect
from urllib.request import urlopen
import re
import redis

def zero_view(request):
    return redirect("/home/")


def home_view(request):
    if request.user.is_authenticated:
        message = "You are logged as " + request.user.username
        is_admin = request.user.is_superuser
    else:
        message = "Welcome, please login."
    context = {
        "message": message,
    }
    return render(request, "home.html", context)


def login_view(request):
    return render(request, "login.html", {})


def logout_view(request):
    logout(request)
    return redirect('/home/')


def login_success_view(request):
    client = redis.Redis(host='localhost', port=6379)
    is_admin = False
    ip_address = ""
    ip_notification_message = ""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            message = "Login Successful!"
            is_admin = request.user.is_superuser
            if is_admin:
                d = str(urlopen('http://checkip.dyndns.com/').read())
                ip_address = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
                last_admin_ip = str(client.get("admin_ip")).lstrip("b'").rstrip("'")
                client.set("admin_ip", ip_address)
                if ip_address == last_admin_ip:
                    ip_notification_message = f"You are logged as an admin and your IP address is {ip_address}"
                else:
                    ip_notification_message = f"You are logged as an admin and your IP address is {ip_address}\n" \
                                              f"Attention. This IP address is different from that used for" \
                                              f" previous admin login ({last_admin_ip})"
        else:
            message = "Credentials are wrong. Try again!"
    else:
        message = "Wrong Request! Please, try again."

    context = {
        "message": message,
        "is_admin": is_admin,
        "ip_address": ip_address,
        "ip_notification_message": ip_notification_message,
    }
    return render(request, "login_success.html", context)
