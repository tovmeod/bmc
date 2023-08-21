from rest_framework import routers

from .views import PassengerViewSet, FareHistogramViewSet

router = routers.DefaultRouter()
router.register('passenger', PassengerViewSet)
router.register(r'fare-histogram', FareHistogramViewSet, basename='fare-histogram')
