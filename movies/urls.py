from django.urls import path
from . import views

urlpatterns = [
    path('<str:category>/<int:page>/', views.browse, name='browse'),
#    path('details/', views.details, name='details')
]

