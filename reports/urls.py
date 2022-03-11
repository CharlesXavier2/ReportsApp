from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/', views.customer, name='customer'),
    path('customer/update', views.CustomerUpdateView.as_view(), name='customer_update'),


    path('reports/', views.reports, name='reports'),
    path('reports/day/', views.day_wise_report, name='daywise_reports'),
    path('reports/item/', views.item_wise_report, name='itemwise_reports'),
    path('reports/subcat/', views.subcat_report, name='subcat_reports'),
    path('reports/cat/', views.cat_report, name='cat_reports'),
    path('reports/daypart/', views.daypart_report, name='daypart_reports'),

    path('items/', views.SelectItems.as_view(), name='order_item'),
    path('items/<int:pk>', views.SelectItems.as_view(), name='order_item'),
    path('items/order/', views.OrderView.as_view(), name='order'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user,  name='login'),
    path('logout', views.logout_user, name = 'logout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)