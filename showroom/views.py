from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Car
from .serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.filter(viewable=True)
    serializer_class = CarSerializer


    @action(detail=False)
    def delete_unavailable(self, request):
        unavailable_cars = Car.objects.filter(viewable=True, available=False)

        for car in unavailable_cars:
            car.viewable = False
            car.save()

        data = {
            'cars_updated': unavailable_cars.count()
        }

        return Response(data=data, status=status.HTTP_200_OK)

    def get_queryset(self):
        """
        Restricts the returned purchases to a given color or make that is viewable
        """
        queryset = Car.objects.filter(viewable=True)

        make = self.request.query_params.get('make', None)
        color = self.request.query_params.get('color', None)
        available = self.request.query_params.get('available', None)

        if make:
            queryset = queryset.filter(car_make=make)
        if color:
            queryset = queryset.filter(color=color)
        if available:
            queryset = queryset.filter(available=available)

        return queryset

    def update(self, request, *args, **kwargs):
        """
        Restricts updates to color and availability only
        """
        instance = self.get_object()
        data = {}

        color = request.data.get('color', None)
        available = request.data.get('available', None)

        if color:
            data['color'] = color
        if available:
            data['available'] = available

        serializer = self.serializer_class(instance, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
