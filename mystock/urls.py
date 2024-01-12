from django.urls import path
from .views import IndexView, ChartsView, TablesView, ResultView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('backtest/', ChartsView.as_view(), name='backtest'),
    path('tables/', TablesView.as_view(), name='tables'),
    path('result/', ResultView.as_view(), name='result'),
]