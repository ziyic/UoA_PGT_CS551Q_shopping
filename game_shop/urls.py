#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Ziyi Cao
# @Time    : 2021/4/26
# @Function:
from django.urls import path, include
import django.contrib.auth.urls
from game_shop import views
from .views import signup

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('carts/', views.carts, name='carts'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('order_list/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('payment/', views.payment, name='payment'),
    path('product/buy/', views.product_buy, name='product_buy'),
    path('product_list/', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('product_new/', views.product_new, name='product_new'),
    path('product/<int:id>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:id>/delete/', views.product_delete, name='product_delete'),
    path('purchase/', views.purchase, name='purchase'),
    path('search/', views.search, name='search'),
]
