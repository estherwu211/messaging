# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Machines
from django.http import HttpResponseRedirect

from influxdb import DataFrameClient
from .forms import table_time_query
import time
#from query import ConsumerQuery
# Create your views here.
#from .forms import NameForm



def morning(request):
    context = {
    }
    return render(request, 'try_jquery.html', context)

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

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = table_time_query(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/display/time_query/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = table_time_query()

    context = {
        'second_list_job_state': second_list_job_state,
        'column_name_job_state': column_name_job_state,
        'second_list_ack': second_list_ack,
        'column_name_ack': column_name_ack,
        'form': form,
    }
    return render(request, 'tables_sidebar.html', context)


# helper function for the main tables
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

    return second_list, column_name


def get_table_time_query(request):
    # get data from forms
    form = table_time_query(request.POST)
    start_time = form['start_time'].value()
    end_time = form['end_time'].value()
    scbds = request.POST.getlist('choose_scoreboard')

    # process choosen scoreboards
    ack_scbd = False
    job_state_scbd = False
    for s in scbds:
        if s == "job_state_scbd":
            job_state_scbd = True
        if s == "ack_scbd":
            ack_scbd = True


    #TODO: add query data
    content = {
        'start_time': start_time,
        'end_time': end_time,
        'ack_scbd': ack_scbd,
        'job_state_scbd': job_state_scbd,
    }

    return render(request, 'name.html', content)

