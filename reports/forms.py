from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import OrderItem, Order, Customer



class SignUpForm(UserCreationForm) : 
    email = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.EmailInput()
    )
    class Meta : 
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm) :
    class Meta : 
        model = User
        fields = ('username', 'password')

class OrderItemForm(forms.ModelForm) :
    
    
    class Meta : 
        model = OrderItem
        fields= ['item', 'quantity']
        labels = {'item': 'Select Product', 'quantity': 'Select Quantity'}

class OrderForm(forms.ModelForm) : 
    class Meta :
        model = Order
        fields = ['items']




class CustomerUpdateForm(forms.ModelForm) : 
    class Meta :
        model = Customer
        fields = ['name', 'contact', 'address']


# iterable 
YEAR_CHOICES = (
    (2021, "2021"), 
    (2022, "2022"),
)
MONTH_CHOICES =( 
    (1, "January"), 
    (2, "February"), 
    (3, "March"), 
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"), 
    (11, "November"), 
    (12, "December"), 
) 
  
# creating a form  
class DayWiseForm(forms.Form): 
    year = forms.ChoiceField(choices = YEAR_CHOICES)
    month = forms.ChoiceField(choices = MONTH_CHOICES)

class ItemSelectForm(forms.Form) :
    item_choice = forms.BooleanField()
    quantity = forms.IntegerField(min_value=1)