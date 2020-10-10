from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework import viewsets
from apps.dht11.models import DHT11
from apps.dht11.serializers import DHT11Serializer

from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
import pandas as pd
import xlsxwriter
import io
from .forms import DHT11Form
from django.http import HttpResponseRedirect


def form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        f = DHT11Form(request.POST)
        # check whether it's valid:
        if f.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/dht11/form/')

    # if a GET (or any other method) we'll create a blank form
    else:
        f = DHT11Form()
    context = {'f': f}
    return render(request, 'dht11/forms.html', context)


class DHT11ViewSet(viewsets.ModelViewSet):
    queryset = DHT11.objects.all()
    serializer_class = DHT11Serializer
    #permission_classes = [permissions.IsAdminUser]


@api_view(['GET'])
def dht11_lates(request):
    try:
        dht11_lates = DHT11.objects.latest('timestamp')
    except DHT11.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = DHT11Serializer(dht11_lates)
        return Response(serializer.data)


def dht11(request):
    nd = [float(item)
          for item in DHT11.objects.values_list('temperature', flat=True)]
    da = [float(item)
          for item in DHT11.objects.values_list('humidity', flat=True)]
    tg = [item.strftime('%Y-%m-%d %H:%M:%S')
          for item in DHT11.objects.values_list('timestamp', flat=True)]
    dht11 = DHT11.objects.all()
    context = {'dht11': dht11,
               'nd': nd,
               'da': da,
               'tg': tg}
    return render(request, 'dht11/dht11.html', context)


def export_dt11_xlsx(request):
    output = io.BytesIO()

    book = xlsxwriter.Workbook(output)
    sheet = book.add_worksheet('DHT11 DataLog')
    row = 0
    sheet.write(row, 0, 'thời gian')
    sheet.write(row, 1, 'nhiệt độ')
    sheet.write(row, 2, 'độ ẩm')

    objects = DHT11.objects.all()

    row += 1
    for item in objects:
        sheet.write(row, 0, (item.timestamp).strftime('%Y-%m-%d %H:%M:%S'))
        sheet.write(row, 1, item.temperature)
        sheet.write(row, 2, item.humidity)
        row += 1
    book.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=dht11_dataLog.xlsx"

    return response


def dht11_to_xlsx(request):

    output_data = {
        'Thời gian cập nhật': [item.strftime('%Y-%m-%d %H:%M:%S') for item in DHT11.objects.values_list('timestamp', flat=True)],
        'Nhiệt độ': [float(item) for item in DHT11.objects.values_list('temperature', flat=True)],
        'Độ ẩm': [float(item) for item in DHT11.objects.values_list('humidity', flat=True)]
    }
    df_dht11 = pd.DataFrame(output_data)
    try:
        from io import BytesIO as IO  # for modern python
    except ImportError:
        from io import StringIO as IO  # for legacy python
    # my "Excel" file, which is an in-memory output file (buffer)
    # for the new workbook
    excel_file = IO()
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df_dht11.to_excel(writer, 'DHT11 DataLog')
    writer.save()
    writer.close()
    # important step, rewind the buffer or when it is read() you'll get nothing
    # but an error message when you try to open your zero length file in Excel
    excel_file.seek(0)
    # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(
    ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # set the file name in the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename=dht11_dataLog.xlsx'

    return response


@csrf_exempt
def dht11_list(request):
    """
    List all code dht11, or create a new dht11.
    """
    if request.method == 'GET':
        dht11s = DHT11.objects.all()
        serializer = DHT11Serializer(dht11s, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DHT11Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def dht11_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        dht11 = DHT11.objects.get(pk=pk)
    except DHT11.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DHT11Serializer(dht11)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DHT11Serializer(dht11, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        dht11.delete()
        return HttpResponse(status=204)
