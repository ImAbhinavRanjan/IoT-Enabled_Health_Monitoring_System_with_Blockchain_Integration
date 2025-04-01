from django.urls import path
from . import views


urlpatterns= [
    
    path("", views.main, name="main"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("logged",views.logged,name="logged"),
    path("latest/<int:user_id>/",views.latest,name="latest"),
    path("get-realtime-data/", views.get_realtime_data, name="get_realtime_data"),
    path("proxy_esp32_data/", views.proxy_esp32_data, name="proxy_esp32_data"),
    path('input/', views.input_health_data, name='input_health_data'),
    path('show/<int:user_id>/', views.show_user_data, name='show_user_data'),
    path('input2/', views.input_health_data_2, name='input_health_data_2'),  
]