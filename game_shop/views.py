import datetime

from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from game_shop.forms import SignUpForm, GameForm
from game_shop.models import Game, Order, LineItem, Cart


# Create your views here.


class TempCart:
    # a data transfer object to shift items from cart to page

    def __init__(self, item_id, name, price, quantity):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f'id: {self.item_id}, name: {self.name}, price: {self.price}, quantity: {self.quantity}'


def product_list(request):
    games = Game.objects.all()
    paginator = Paginator(games, 25)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    cart = request.session.get('Cart', [])
    request.session['Cart'] = cart
    deleted = request.session.get('deleted', 'empty')
    request.session['deleted'] = 'hello'

    return render(request, 'game_shop/game_list.html', {'games': page, 'deleted': deleted})


def get_cart(request):
    cart = request.session.get('Cart', [])
    products = []
    for item in cart:
        print(item[0])
        product = Game.objects.get(id=item[0])
        cart_line = TempCart(item[0], product.name, product.price, item[1])
        products.append(cart_line)
        print(products[0])
    return products


def carts(request):
    games = get_cart(request)
    return render(request, 'game_shop/cart.html', {'games': games})


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.customer.first_name = form.cleaned_data.get('first_name')
        user.customer.last_name = form.cleaned_data.get('last_name')
        user.customer.address = form.cleaned_data.get('address')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'registration/signup.html', {'form': form})


def dashboard(request):
    orders = Order.objects.all()
    user = request.user
    days = []
    for day in range(-14, 0, 1):
        days.append(datetime.datetime.now().date() + datetime.timedelta(days=day))
    dataset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for order in orders:
        print(order.created_date)
        for i in range(len(days)):
            if order.created_date == days[i]:
                dataset[i] += 1

    if user.is_authenticated & user.is_staff:
        print(days)
        print(dataset)
        return render(request, 'game_shop/dashboard.html', {'days': days, 'dataset': dataset})
    else:
        return redirect('accounts/login.html')


def customer_list(request):
    users = User.objects.all()
    return render(request, 'game_shop/customer_list.html', {'customers': users})


def customer_detail(request, customer_id):
    user = get_object_or_404(User, id=customer_id)
    return render(request, 'game_shop/customer_detail.html', {'customer': user})


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'game_shop/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer
    user = get_object_or_404(User, id=customer.pk)
    # TODO: modify order structure
    line_items = LineItem.objects.filter(order_id=order.id)
    return render(request, 'game_shop/order_detail.html', {'order': order, 'customer': user, 'line_items': line_items})


def payment(request):
    games = get_cart(request)
    user = request.user
    order = Order.objects.create(customer=user.customer)
    order.refresh_from_db()
    for game in games:
        product_item = get_object_or_404(Game, id=game.item_id)
        cart = Cart.objects.create(item=product_item, quantity=game.quantity)
        cart.refresh_from_db()
        line_item = LineItem.objects.create(quantity=game.quantity, product=product_item,
                                            cart=cart, order=order)

    request.session['Cart'].clear()
    request.session['deleted'] = 'thanks for your purchase'
    return redirect('product_list')


def product_buy(request):
    if request.method == "POST":
        temp_id = int(request.POST.get('id', ''))
        quantity = int(request.POST.get('quantity', ''))
        if not request.session.get('Cart'):
            request.session['Cart'] = []
        cart = request.session['Cart']
        cart.append([temp_id, quantity])
        request.session['Cart'] = cart
        print(cart)
    return redirect('product_list')


def product_detail(request, id):
    game = get_object_or_404(Game, id=id)
    overall = game.positive_ratings + game.negative_ratings
    if game.positive_ratings / overall >= 0.95:
        reputation = 'Overwhelmingly Positive'
        colour = '#547DAE'
    elif game.positive_ratings / overall >= 0.8:
        reputation = 'Very Positive'
        colour = '#547DAE'
    elif game.positive_ratings / overall >= 0.7:
        reputation = 'Mostly Positive'
        colour = '#547DAE'
    elif game.positive_ratings / overall >= 0.4:
        reputation = 'Mixed'
        colour = '#D4A24E'
    elif game.positive_ratings / overall >= 0.2:
        reputation = 'Mostly Negative'
        colour = '#AA3C32'
    else:
        reputation = 'Very Negative'
        colour = '#AA3C32'
    return render(request, 'game_shop/product_detail.html', {'product': game,
                                                             'reputation': reputation,
                                                             'colour': colour})


def product_new(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            return redirect('product_detail', id=product.id)
    else:
        form = GameForm()
    return render(request, 'game_shop/product_edit.html', {'form': form})


def product_edit(request, id):
    product = get_object_or_404(Game, id=id)
    if request.method == "POST":
        form = GameForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            return redirect('product_detail', id=product.id)
    else:
        form = GameForm(instance=product)
    return render(request, 'game_shop/product_edit.html', {'form': form})


def product_delete(request, id):
    product = get_object_or_404(Game, id=id)
    deleted = request.session.get('deleted', 'empty')
    request.session['deleted'] = product.name
    product.delete()
    return redirect('product_list')


def purchase(request):
    if request.user.is_authenticated:
        user = request.user
        products = get_cart(request)
        total = 0
        for product in products:
            total += product.price * product.quantity
        return render(request, 'game_shop/purchase.html', {'products': products, 'customer': user, 'total': total})
    else:
        return redirect('login')


def index(request):
    title = 'Game shop'
    return render(request, 'game_shop/index.html', {'title': title})


def search(request):
    result = []
    if request.method == 'GET':
        form_key = request.GET.get('searchbar')
        result = Game.objects.filter(name__icontains=form_key)
    deleted = request.session.get('deleted', 'empty')
    request.session['deleted'] = 'hello'
    return render(request, 'game_shop/game_list.html', {'games': result, 'delete': deleted})
