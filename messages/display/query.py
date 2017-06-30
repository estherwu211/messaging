from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from influxdb import DataFrameClient
import time

class ConsumerQuery:
  def __init__(self, request):
    while 1:
        self.publish_page(request)
        time.sleep(30)


  def publish_page(self, request):
      influx_db = "estherdb"
      self.second_list_job_state, self.column_name_job_state = self.get_query_result("JOB_STATE", influx_db)
      self.second_list_ack, self.column_name_ack = self.get_query_result("acks", influx_db)
      context = {
          'second_list_job_state': self.second_list_job_state,
          'column_name_job_state': self.column_name_job_state,
          'second_list_ack': self.second_list_ack,
          'column_name_ack': self.column_name_ack,
      }
      return render(request, 'tables_sidebar.html', context)

  def get_query_result(self, measurement_name, influx_db):
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