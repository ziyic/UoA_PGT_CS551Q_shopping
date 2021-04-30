# Created by Ziyi Cao at 2021/4/29
Feature: Cart

  Scenario: Add game to Cart
    # Enter steps here
    Given : we have logged in with a user and we are at game details page

    When : we set a quantity and click on Purchase link

    Then : game has been add to the cart