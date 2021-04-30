#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Ziyi Cao
# @Time    : 2021/4/29
# @Function:
from behave import *

use_step_matcher("re")


@given(": we have logged in with a user and we are at game details page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get('http://localhost:8000/accounts/login/')
    name_textfield = context.browser.find_element_by_name('username')
    name_textfield.send_keys('Douglas Phillips')
    price_textfield = context.browser.find_element_by_name('password')
    price_textfield.send_keys('8B8qXwYuVNGAwK')
    context.browser.find_element_by_name('Login').click()
    context.browser.get('http://localhost:8000/product/1/')


@when(": we set a quantity and click on Purchase link")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    quantity_textfield = context.browser.find_element_by_id('quantity')
    quantity_textfield.send_keys('1')
    context.browser.find_element_by_id('Purchase').click()


@then(": game has been add to the cart")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get('http://localhost:8000/carts/')
    assert context.browser.find_element_by_id('cart_item')
