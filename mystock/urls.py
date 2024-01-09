from django.urls import path
from .views import IndexView, ChartsView, TablesView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('charts/', ChartsView.as_view(), name='charts'),
    path('tables/', TablesView.as_view(), name='tables'),
]