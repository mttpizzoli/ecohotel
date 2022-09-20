from django.shortcuts import render
from django.contrib.auth.models import Group
from django.http import JsonResponse
from .models import MeterReading
import requests


def log_en(request):
    past_readings_number = len(MeterReading.objects.all())
    if request.method == "POST":
        produced_energy_in_wh = request.POST["produced-energy"]
        consumed_energy_in_wh = request.POST["consumed-energy"]
        MeterReading.objects.create(produced_energy_in_wh=produced_energy_in_wh,
                                    consumed_energy_in_wh=consumed_energy_in_wh,
                                    id=past_readings_number+1)
        message = "{" + f"produced_energy_in_wh: {produced_energy_in_wh}," \
                  f"consumed_energy_in_wh: {consumed_energy_in_wh}" + "}"
        MeterReading.objects.get(id=past_readings_number+1).get_timestamp()
        MeterReading.objects.get(id=past_readings_number+1).send_transaction(message)
        timestamp_last_log = MeterReading.objects.get(id=past_readings_number+1).timestamp
    else:
        if past_readings_number == 0:
            timestamp_last_log = "Never"
        else:
            timestamp_last_log = MeterReading.objects.get(id=past_readings_number).timestamp

    user = request.user
    operators_group = Group.objects.filter(name="Operators").get(name="Operators")
    try:
        is_an_operator = operators_group == user.groups.all().get(name="Operators")
    except(Group.DoesNotExist):
        is_an_operator = False

    context = {
        "is_an_operator": is_an_operator,
        "timestamp_last_log": timestamp_last_log,
    }
    return render(request, "log_en.html", context)


def endpoint(request):
    past_readings_number = len(MeterReading.objects.all())
    last_reading = MeterReading.objects.get(id=past_readings_number)

    produced_energy_last_day = last_reading.produced_energy_in_wh
    consumed_energy_last_day = last_reading.consumed_energy_in_wh
    transaction_id = last_reading.transaction_id

    context = {
            "produced_energy_in_wh": produced_energy_last_day,
            "consumed_energy_in_wh": consumed_energy_last_day,
            "transaction_id": transaction_id,
        }
    return JsonResponse(context)


def data_last_24h_view(request):
    response = {}
    is_authenticated = request.user.is_authenticated
    url = request.scheme + "://" + request.get_host() + "/endpoint"
    try:
        response = requests.get(url=url).json()
    except:
        response["produced_energy_in_wh"] = ""
        response["consumed_energy_in_wh"] = ""
        response["transaction_id"] = ""

    context = {
        "is_authenticated": is_authenticated,
        "produced_energy":  response["produced_energy_in_wh"],
        "consumed_energy": response["consumed_energy_in_wh"],
        "transaction_id": response["transaction_id"],
    }

    return render(request, "data.html", context)


def data_all_time_view(request):
    is_admin = request.user.is_superuser
    all_readings = MeterReading.objects.all()
    total_produced_energy = 0
    total_consumed_energy = 0
    for item in all_readings:
        total_produced_energy += item.produced_energy_in_wh
        total_consumed_energy += item.consumed_energy_in_wh
    context = {
        "is_admin": is_admin,
        "total_produced_energy": total_produced_energy,
        "total_consumed_energy": total_consumed_energy,
    }
    return render(request, "data_all_time.html", context)
