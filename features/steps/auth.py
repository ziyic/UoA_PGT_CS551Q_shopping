#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Ziyi Cao
# @Time    : 2021/4/29
# @Function:
from urllib.parse import urljoin

from behave import *

use_step_matcher("re")


@given(": when we at user login page")
def locate_to_loginPage(context):
    """
    :type context: behave.runner.Context
    """
    # url = urljoin(context.test_case.live_server_url, '/login/')
    context.browser.get('http://localhost:8000/accounts/login/')


@when(": we input username and password")
def input_login_details(context):
    """
    :type context: behave.runner.Context
    """

    # print(context.browser.page_source)
    name_textfield = context.browser.find_element_by_name('username')
    name_textfield.send_keys('Douglas Phillips')
    price_textfield = context.browser.find_element_by_name('password')
    price_textfield.send_keys('8B8qXwYuVNGAwK')
    context.browser.find_element_by_name('Login').click()


@when(": we input a superuser username and password")
def input_superuser_login_details(context):
    """
    :type context: behave.runner.Context
    """
    # print(context.browser.page_source)
    name_textfield = context.browser.find_element_by_name('username')
    print(name_textfield)
    name_textfield.send_keys('superuser')
    price_textfield = context.browser.find_element_by_name('password')
    price_textfield.send_keys('superuser')
    context.browser.find_element_by_name('Login').click()


@then(": we can see application has been logged in")
def user_logged_in(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element_by_id('greeting_info')


@then(": we can see application has been logged in with a superuser")
def user_logged_in(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element_by_id('greeting_info')


@given(": when we logged in with a user")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element_by_id('greeting_info')


@when(": we click on logout link")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_element_by_partial_link_text('Log Out').click()


@then(": we can see application has been logged out")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element_by_partial_link_text('Log In')
