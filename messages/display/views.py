# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Machines

from influxdb import DataFrameClient
import time
#from query import ConsumerQuery
# Create your views here.




def morning(request):
    return HttpResponse("<h1>It's morning right now :) HEY</h1>")

def view_forwarders(request, forwarder_id):
    #m = get_object_or_404(Machines,forwarder_id = forwarder_id)
    pic_dict = {
        'IDLE': '"images/rvn.jpg"',
        'WORKING': '"images/glazed.jpg"',
        'BAD': '"images/felix.jpg"',
    }
    all_machines = Machines.objects.all()
    machine_chosen = []
    for machine in all_machines:
        if machine.forwarder_id == forwarder_id:
            machine_chosen.append(machine)
    machine_chosen.reverse()

    context = {
        'forwarder_id': forwarder_id,
        'machine_chosen': machine_chosen,
    }
    return render(request, 'forwarders.html', context)

def view_scoreboard(request):
    #m = get_object_or_404(Machines,forwarder_id = forwarder_id)
    influx_db = "estherdb"
    second_list_job_state, column_name_job_state = get_query_result(measurement_name="JOB_STATE", influx_db=influx_db)
    second_list_ack, column_name_ack = get_query_result(measurement_name="acks", influx_db=influx_db)
    context = {
        'second_list_job_state': second_list_job_state,
        'column_name_job_state': column_name_job_state,
        'second_list_ack': second_list_ack,
        'column_name_ack': column_name_ack,
    }
    return render(request, 'tables_sidebar.html', context)



def get_query_result(measurement_name, influx_db):
    # get result as a dataframe
    client = DataFrameClient(host='141.142.211.122', port=8086, database=influx_db)
    query_message = "select * from {0};".format(measurement_name)

    # extract the result from dataframe
    query_result = client.query(query_message)[measurement_name]
    # make in to correct form
    column_name = list(query_result)
    second_list = []
    for index, row in query_result.iterrows():
        first_list = []
        first_list.append(str(index))
        for c in column_name:
            first_list.append(row[c])
        second_list.append(first_list)

    column_name = list(query_result)
    print(second_list)
    return second_list, column_name