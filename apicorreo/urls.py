from django.urls import path
from . import views
urlpatterns = [

    path('obtener_valores_bl/', views.registros, name='bl'),
    path('obtener_token/', views.ObtenerToken, name='token'),
    path('obtener_urls/', views.ObtenerUrls, name='url'),
   
]