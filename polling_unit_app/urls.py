from django.urls import path
from . import views

urlpatterns = [
    path('<int:polling_unit_id>/', views.polling_unit_results, name='polling_unit_results'),
    path('local_government_results/', views.local_government_results, name='local_government_results'),
    path('add_polling_unit_result/', views.add_polling_unit_result, name='add_polling_unit_result'),
]
