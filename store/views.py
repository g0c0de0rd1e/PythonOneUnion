from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Item
from .paginator import paginator

from cart.views import Cart
from checkout.forms import OrderCreateForm
from checkout.models import Order, OrderItem, ShippingAddress

def store(request):
    items = Item.objects.filter(is_available=True)
    context = {
        'page_obj': paginator(request, items, 9),
        'range': [*range(1, 7)],  # For random css styles
    }

    return render(request, 'store/main_page.html', context)


def item_details(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    context = {
        'item': item,
    }
    return render(request, 'store/item_details.html', context)


def tag_details(request, slug):
    tag = get_object_or_404(ItemTag, slug=slug)
    items = Item.objects.filter(tags__in=[tag])
    context = {
        'tag': tag,
        'page_obj': paginator(request, items, 3),
    }
    return render(request, 'store/tag_details.html', context)


def tag_list(request):
    tags = ItemTag.objects.all()
    context = {
        'page_obj': paginator(request, tags, 6),
    }
    return render(request, 'store/tag_list.html', context)

@login_required
def create_order(request, *args, **kwargs):
    item_slug = kwargs.get('item_slug')
    try:
        item = Item.objects.get(slug=item_slug)
    except Item.DoesNotExist:
        return redirect('/')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Создаем новый заказ
            order = Order.objects.create(
                payment_method=form.cleaned_data['payment_method'],
                user=request.user,
            )

            # Создаем адрес доставки
            shipping_address = ShippingAddress.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address_line_1=form.cleaned_data['address_line_1'],
                address_line_2=form.cleaned_data['address_line_2'],
                order=order,
            )

            # Создаем товары в заказе
            for item_id, quantity in form.cleaned_data['items']:
                item = Item.objects.get(id=item_id)
                OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=quantity,
                    price=item.price
                )

            # Очищаем корзину
            request.session.pop('cart', None)

            # Редирект на страницу благодарности
            return redirect('checkout:thank_you', order_id=order.id)
    
    # Если это GET-запрос или форма не была отправлена
    form = OrderCreateForm(initial={
        'items': [(item.id, 1)],  # Товар и его количество
    })
    quantity = 1 
    return render(request, 'checkout/checkout.html', 
        {'form': form,
         'item': item,
         'quantity': quantity})