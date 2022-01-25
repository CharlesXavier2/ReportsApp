from django.contrib.auth.forms import AuthenticationForm
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import date
from django.utils import timezone
from django.db.models import Count
from django.views.generic.base import View
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone

from .utils import MONTH_CHOICES, YEAR_CHOICES, DAYPART_CHOICES, DAYPART_RANGES

# Create your views here.

from .models import Category, SubCategory, Item, Order, OrderItem, Customer
from .forms import OrderItemForm, OrderForm, SignUpForm, LoginForm, DayWiseForm
def home(request) :
    c = Customer.objects.all()
    print(c)
    user = request.user
    cat = Category.objects.all()
    sub = SubCategory.objects.all()
    
    return render(request, 'reports/home.html', {'user' : user, 'categories': cat, 'subcategories': sub})

def customer(request) :
    
    user = request.user
    customer = user.customer
    orders = Order.objects.filter(user = user).order_by('-created_at')
    count = len(orders)
    return render(request, 'reports/customer.html', {'customer' : customer, 'count':count, 'orders': orders})
item_list = []
def order_item(request) :
    user = request.user
    
    if request.method == 'POST' :
        form = OrderItemForm(request.POST)
        if form.is_valid() :
            order_product = form.save(commit=False)
            print('OrderItem Created', order_product.item, order_product.quantity)
            
            item = OrderItem(
                quantity = form.cleaned_data['quantity'],
                item = form.cleaned_data['item']
            )
            item.save()
            print("ID", item.id)
            
            item_list.append(item) 
            form = OrderItemForm()
            add_msg = "Add Another Item"
    else :
        form = OrderItemForm()
        add_msg = "Add Item"
    return render(request, 'reports/order_item.html', {'items': item_list, 'form': form, 'add_msg': add_msg})

class SelectItems(View) :
    items = Item.objects.all()
    def get(self, request, *args, **kwargs) :
        
        return render(request, 'reports/order_item.html', {'items': self.items})

    def post(self, request, *args, **kwargs) :
        
        item_id = request.POST.get('item')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        increase = request.POST.get('increase')
        if cart :
            quantity = cart.get(item_id)
            if quantity :
                if remove :
                    if quantity <= 1 : cart.pop(item_id)
                    else : cart[item_id] = quantity - 1
                elif increase : 
                    cart[item_id] = quantity + 1
                else : 
                    cart[item_id] = quantity + 1
            else :
                cart[item_id] = 1

        else :
            cart = {}
            cart[item_id] = 1
        request.session['cart'] = cart
        keys = request.session['cart'].keys()
        print(keys)
        print('Cart', request.session['cart'])
        
        return render(request, 'reports/order_item.html', {'items': self.items})


class OrderView(View) :
    
    def get(self, request, *args, **kwargs) :
        items= []
        total = 0
        user = request.user
        cart = request.session.get('cart')
        customer = Customer.objects.get(user = user)
        for i, quantity in cart.items() :
            item = Item.objects.get(pk = int(i))
            items.append({
                'item' : item,
                'quantity' : quantity,
                'price' : quantity * item.price
            })
            total +=quantity * item.price
        return render(request, 'reports/order.html', {'customer': customer, 'items' : items, 'total': total})

    def post(self, request, *args, **kwargs) :
        order_items = []
        user = request.user
        cart = request.session.get('cart')
        customer = Customer.objects.get(user = user)
        name = request.POST.get('cname')
        contact = request.POST.get('ccontact')
        address = request.POST.get('address')
        for i, quantity in cart.items() :
            item = Item.objects.get(pk = int(i))
            oi = OrderItem.objects.create(item=item, quantity=quantity)
            order_items.append(oi)
        
        instance = Order.objects.create(
            user = user,
            created_at = timezone.now(),
            contact= contact,
            address= address

        )
        instance.items.add(*order_items)
        cart={}
        request.session['cart'] = cart
        return redirect('customer')
        

################################## REPORTS SECTION #######################################################################

def reports(request) :
    user = request.user
    if user.is_staff == True :
        total_sales = 0

        orders = Order.objects.order_by('-created_at')
        count = len(orders)
        for order in orders :
            total_sales += order.get_total_price()
            
        return render(request, 'reports/reports.html', {'user' : user, 'sales' : total_sales, 'count': count})
    else :
        msg1 = "Not Authorised"
        msg2 ='Only Staffs are permitted to view reports. Please login with a staff account'
        messages.add_message(request, messages.ERROR, msg1 )
        messages.info(request, msg2)
        return redirect('login')

def day_wise_report(request):
    user = request.user
    if user.is_staff == True :
        count = 0
        total = 0
        queryset = []
        if request.method == 'POST':
            fm = DayWiseForm(request.POST)
            orders = {}
            design = {}
            report = []
            total_sales = 0
            total_orders = 0
            if fm.is_valid():
                day = 1
                month = fm.cleaned_data['month']
                year = fm.cleaned_data['year']
                while day <= 31:
                    queryset = Order.objects.filter(
                        created_at__month=month, created_at__year=year, created_at__day=day)
                    if queryset.exists():
                        orders[day] = queryset
                    else : orders[day] =""
                    day += 1
                
                for day, list_orders in orders.items():
                    day_format = str(day) + ' ' +MONTH_CHOICES[int(month)]
                    if list_orders != "" :
                        
                        count = 0
                        total = 0
                        for order in list_orders:
                            
                            count += 1
                            
                            total += order.get_total_price()
                        total_orders += count
                        total_sales += total
                            
                        report.append({'day': day_format, 'count': count, 'total': total})
                    else :
                        report.append({'day': day_format, 'count': 0, 'total': 0})
                
            return render(request, 'reports/daywise_report.html', {'month': MONTH_CHOICES[int(month)],'count': total_orders, 'total': total_sales, 'form': fm, 'orders': report})
        else:
            fm = DayWiseForm()
            return render(request, 'reports/daywise_report.html', {'month': '','count': count, 'total': total, 'form': fm})
    else :
        return redirect('login')

def cat_report(request) :
    user = request.user
    if user.is_staff == True :
        reports = []
        total_sales = 0
        
        cats = Category.objects.all()
        for cat in cats :
            sub_sales = 0
            sub_quantity = 0
            subcats = cat.subcategories.all()
            for subcat in subcats :
                items = subcat.items.all()
                for item in items :
                    quantity = 0
                    item_sales = 0
                    oi_list = item.orderitems.all()
                    for oi in oi_list :
                        quantity += oi.quantity
                    item_sales = item.price * quantity
                    sub_sales += item_sales
                    sub_quantity += quantity
                    total_sales += item_sales
            reports.append({
                'name' : cat.name,
                    
                'quantity' : sub_quantity,
                'sales' : sub_sales
            })
        print(reports)
        return render(request, 'reports/cat_report.html', {'reports': reports, 'total_sales': total_sales})
    else :
        return redirect('login')

def item_wise_report(request) :
    user = request.user
    if user.is_staff == True :
        reports = []
        total_sales = 0
        items = Item.objects.all()
        for item in items :
            quantity = 0
            sales = 0
            oi_list = item.orderitems.all()
            for oi in oi_list :
                quantity += oi.quantity
            sales = item.price * quantity
            total_sales += sales
            reports.append({
                'name' : item.name,
                'subcat_name' : item.subcategory.name,
                'quantity' : quantity,
                'sales' : sales
            })
        print(reports)
        return render(request, 'reports/itemwise_report.html', {'reports': reports, 'total_sales': total_sales})
    else :
        return redirect('login')

def subcat_report(request) :
    user = request.user
    if user.is_staff == True :
        reports = []
        total_sales = 0
        subcats = SubCategory.objects.all()
        for subcat in subcats :
            items = subcat.items.all()
            for item in items :
                quantity = 0
                sales = 0
                oi_list = item.orderitems.all()
                for oi in oi_list :
                    quantity += oi.quantity
                sales = item.price * quantity
                total_sales += sales
                reports.append({
                    'name' : subcat.name,
                    'cat_name' : subcat.category.name,
                    'quantity' : quantity,
                    'sales' : sales
                })
        print(reports)
        return render(request, 'reports/subcat_report.html', {'reports': reports, 'total_sales': total_sales})
    else :
        return redirect('login')

def daypart_report(request) :
    #data = Order.m_objects.get_day_set(1)
    data = Order.objects.values('created_at__day').annotate(x = Sum('items__item__price'))
    total_sales= 0
    i = 1
    order_list = []
    while i <= 4 :
        queryset = Order.objects.filter(created_at__hour__range = DAYPART_RANGES[i])
        if queryset.exists() :
            count = 0
            sales = 0
            for order in queryset :
                count += 1
                sales += order.get_total_price()
            order_list.append({
                'daypart' : DAYPART_CHOICES[i],
                'count' : count,
                'sales' : sales,
            })
            total_sales += sales
        else :
            order_list.append({
                'daypart' : DAYPART_CHOICES[i],
                'count' : 0,
                'sales' : 0,
            })
        i += 1
    
    print(data)
    return render(request, 'reports/daypart_report.html', {'reports' : order_list, 'total_sales': total_sales})
################################### AUTH SECTION ######################################################################

def signup(request) :
    if request.method == "POST" :
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid() : 
            user = signup_form.save()
            login(request, user)
            return redirect('home')
    else:
        signup_form = SignUpForm()
    return render(request, 'reports/signup.html', {'form': signup_form})

def login_user(request) :
    if request.method == "POST" :
        login_form = AuthenticationForm(request = request, data=request.POST)
        if login_form.is_valid() : 
            uname = login_form.cleaned_data['username']
            upass = login_form.cleaned_data['password']
            user = authenticate(username = uname, password = upass)
            if user is not None :
                login(request, user)
                return redirect('home')
    else:
        login_form = AuthenticationForm()
    return render(request, 'reports/login.html', {'form': login_form})

def logout_user(request) :
    if request.user.is_authenticated :
        logout(request)
        request.session.clear_expired()
        return redirect('home')
    else :
        return redirect('login')
