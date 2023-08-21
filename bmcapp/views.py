import io

import pandas
from django.core.exceptions import FieldDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse
from matplotlib import pyplot

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Passenger
from .serializers import PassengerSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    lookup_field = 'PassengerId'

    def get_queryset(self):
        queryset = super().get_queryset()
        fields_param = self.request.query_params.getlist('fields')

        if fields_param:
            # Filter the queryset to query only the specified fields
            queryset = queryset.only(*fields_param)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except FieldDoesNotExist:
            return HttpResponseBadRequest()
        serializer = self.get_serializer(instance,
                                         context={'selected_fields': self.request.query_params.getlist('fields')})
        return Response(serializer.data)


class FareHistogramViewSet(viewsets.ViewSet):
    percentiles = [25, 50, 75, 80, 90, 95, 99]

    def list(self, request):
        fare_prices = Passenger.objects.values_list('Fare', flat=True)
        # Convert to float because quantile does not play nice with Decimal
        fare_series = pandas.Series([float(fare) for fare in fare_prices])

        fare_percentiles = fare_series.quantile([p / 100 for p in self.percentiles])

        # Create a histogram using the calculated percentiles
        pyplot.bar(self.percentiles, fare_percentiles)
        pyplot.xlabel('Percentile')
        pyplot.ylabel('Fare')
        pyplot.title('Histogram of Fare Prices in Percentiles')
        pyplot.xticks(self.percentiles, [f'{p}%' for p in self.percentiles])

        # Save the plot as an image
        png_buffer = io.BytesIO()
        pyplot.savefig(png_buffer, format='png')
        pyplot.close()

        response = HttpResponse(png_buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'inline; filename="histogram.png"'
        return response

    def histogram_data_to_png(self, histogram_data):
        pyplot.bar([str(p) + '%' for p in self.percentiles], [data['count'] for data in histogram_data])
        pyplot.xlabel('Percentile')
        pyplot.ylabel('Count')
        pyplot.title('Fare Price Histogram')
        pyplot.tight_layout()

        # Save the plot as an image
        buffer = io.BytesIO()
        pyplot.savefig(buffer, format='png')
        pyplot.close()
        return buffer
