#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Ziyi Cao
# @Time    : 2021/4/29
# @Function:

from behave import *

use_step_matcher("re")


@given("we want to find a game")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get('http://localhost:8000/')
    assert context.browser.find_element_by_id('searchbar')


@when("we fill in the name of the into search bar")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    searchbar = context.browser.find_element_by_name('searchbar')
    searchbar.send_keys('Counter-Strike')
    context.browser.find_element_by_id('searchbarSubmit').click()


@then("show the search result")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.find_element_by_id('game_item')


@given("we are at a game list page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.get('http://localhost:8000/product_list/')


@when("we click on one of the game name")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.browser.find_element_by_partial_link_text('Counter-Strike').click()


@then("we will be redirect to game detail")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.browser.current_url == 'http://localhost:8000/product/1/'
