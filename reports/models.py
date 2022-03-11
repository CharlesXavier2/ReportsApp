from django.db import models
from django.db.models import fields
from django.db.models.fields import CharField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Category(models.Model) :
    name = models.CharField(max_length=30, unique=True)
    def __str__(self) :
        return self.name
    
    def get_subs_count(self):
        return SubCategory.objects.filter(category_id=self).count()

class SubCategory(models.Model) :
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    def __str__(self) :
        return self.name

class Item(models.Model) :
    name = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='menu_images/', default='/menu_images/item_default.png')
    subcategory = models.ForeignKey(SubCategory, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)
    is_veg = models.BooleanField(default=True)
    def __str__(self) :
        return self.name

def validate_quantity(value) :
    if value < 1 :
        raise ValidationError('Quantity should atleast be 1')

class OrderItem(models.Model) :
    item = models.ForeignKey(Item, related_name='orderitems', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[validate_quantity])

    def __str__(self) :
        return self.item.name + '-' + str(self.quantity)

    def get_item_quantity_price(self) : 
        return self.quantity * self.item.price
    


   
class Customer(models.Model) :
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE)
    address =  models.CharField(max_length=300)
    contact = models.CharField(max_length=10)

    def __str__(self) :
        return self.name

class OrderManager(models.Manager) :
    def get_day_set(self, day) :
        return self.filter(created_at__day = day)

class Order(models.Model) :
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    
    items = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField()
    address =  models.CharField(max_length=300, null=True)
    contact = models.CharField(max_length=10, null= True)

    objects = models.Manager()
    m_objects = OrderManager()
    def get_total_price(self) :
        total = 0
        for order_item in self.items.all() :
            total += order_item.get_item_quantity_price()
        return total

    def __str__(self) :
        return self.user.username + '-' + str(self.get_total_price()) +'Rs.'

    def get_items(self):
        return ",".join([p.item.name for p in self.items.all()])
    
    def get_items_with_quantity(self) :
        data = ""
        for oi in self.items.all() :
            data += oi.item.name + "-" + str(oi.quantity) + ","
        return data


 