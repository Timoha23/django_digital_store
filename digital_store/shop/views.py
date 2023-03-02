from django.shortcuts import render

def index(request):
    return render(request, template_name='shop/index.html')

def shop(request, shop_name):
    print(shop_name)
    return render(request, template_name='shop/shop.html')

def item(request, item_id):
    print(item_id)
    return render(request, template_name='shop/item.html')
