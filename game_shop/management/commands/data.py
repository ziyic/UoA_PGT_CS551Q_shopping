#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Ziyi Cao
# @Time    : 2021/4/25
# @Function:
import os
import random
import decimal
import string
import pandas as pd

from random import choice
from datetime import datetime
from pathlib import Path

from django.db import models
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from game_shop.models import Cart, Customer, LineItem, Order, Game


def GenPassword(length=8, charset=string.ascii_letters + string.digits):
    password = ''.join([choice(charset) for i in range(length)])
    return password


class Command(BaseCommand):
    help = 'Load data into the tables'

    def handle(self, *args, **options):
        Cart.objects.all().delete()
        LineItem.objects.all().delete()
        Order.objects.all().delete()
        Game.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()

        print("tables dropped successfully")

        base_dir = Path(__file__).resolve().parents[3]

        fake = Faker()

        game_data = pd.read_csv(str(base_dir) + '/game_shop/steam.csv')

        # create some customers
        for i in range(20):
            first_name = str(fake.first_name()).lstrip("[|'| |((").rstrip("]|'| |)"),
            last_name = str(fake.last_name()).lstrip("[|'| |(").rstrip("]|'| |)|,"),
            username = first_name[0] + ' ' + last_name[0],
            password = GenPassword(length=random.randint(8, 16))
            user = User.objects.create_user(
                username=username[0],
                first_name=first_name[0],
                last_name=last_name[0],
                email=fake.ascii_free_email(),
                password=password)
            customer = Customer.objects.get(user=user)
            address = fake.address().lstrip("[|'| |(").rstrip("]|'| |)"),
            customer.address = address[0]
            customer.save()
            print(customer.user.username, password)

        # create some products
        for i in range(0, 2000):
            achievements = True if game_data.iloc[i]['achievements'] == 0 else False
            game = Game.objects.create(
                name=game_data.iloc[i]['name'],
                Release_date=game_data.iloc[i]['release_date'],
                Required_age=game_data.iloc[i]['required_age'],
                achievements=achievements,
                positive_ratings=game_data.iloc[i]['positive_ratings'],
                negative_ratings=game_data.iloc[i]['negative_ratings'],
                average_playtime=game_data.iloc[i]['average_playtime'],
                price=game_data.iloc[i]['price'],
            )
            game.save()
            print(game)

        # create some carts
        products = list(Game.objects.all())
        for i in range(10):
            random_id = random.randint(1, len(products))
            cart = Cart.objects.create(
                item=products[random_id],
                quantity=random.randrange(1, 99),
            )
            cart.save()
        print("Cart ready")

        # create orders from customers
        customers = Customer.objects.all()
        for customer in customers:
            for i in range(random.randint(1, 5)):
                order = Order.objects.create(
                    customer=customer,
                )
                order.save()
        print("Order.customers ready")

        # attach line_items to orders
        orders = Order.objects.all()
        carts = Cart.objects.all()
        for order in orders:
            for cart in carts:
                line_item = LineItem.objects.create(
                    quantity=cart.quantity,
                    product=cart.item,
                    cart=cart,
                    order=order,
                )
                line_item.save()

        print("tables successfully loaded")
