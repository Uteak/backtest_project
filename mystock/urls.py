from django.urls import path
from .views import IndexView, ChartsView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('charts/', ChartsView.as_view(), name='charts'),
]