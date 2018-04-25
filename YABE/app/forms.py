"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

CATAGORY_CHOICES = [('1','Bookstore'),('2','Collectibles & Art'),
               ('3','Electronic'),('4','Fashion'),
               ('5','Home & Garden'),('6','Sporting Goods'),
               ('7','Toys & Hobbies'),('8','Others')]
GENDER_CHOICES = [('1','Male'),('2','Female')]
INCOME_CHOICES = [('1','<50,000'),('2','50,000-100,000'),('3','100,000-200,000'),('4','>200,000')]


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    

    class RegisterNewUser(AuthenticationForm):
        """Authentication form which uses boostrap CSS."""
        username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
        password = forms.CharField(label=_("Password"),
                                   widget=forms.PasswordInput({
                                       'class': 'form-control',
                                       'placeholder':'Password'}))
class AddUserForm(forms.Form):
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES)
    annualIncome = forms.ChoiceField(widget=forms.RadioSelect, choices=INCOME_CHOICES)
    age = forms.IntegerField(max_value = 120, min_value = 5)

    
class AddItemForm(forms.Form):
    itemname= forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Item name'}))
    price = forms.DecimalField(label = _(' Price'))

    quantity = forms.IntegerField(label = _('Quantity: '),min_value = 0,
                                 widget = forms.NumberInput({
                                   'class': 'form-control',
                                   'placeholder': 'Quantity of Item'}))

    isVirtual = forms.BooleanField(label = _('is Virtual Item?: '),
                                    required=False)
    '''
    picture = forms.ImageField(label=_('Description Image'),
                               required=False,
                              error_messages = {'invalid':_("Image files only")})
    '''
    picture = forms.ImageField()
    description = forms.CharField(max_length=1000,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Item name'}))

    category = forms.ChoiceField(widget=forms.RadioSelect, choices=CATAGORY_CHOICES)


class AddBiddingItemForm(forms.Form):
    itemname= forms.CharField(max_length=254,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Item name'}))


    isVirtual = forms.BooleanField(label = _('is Virtual Item?: '),
                                    required=False)

    picture = forms.ImageField()

    description = forms.CharField(max_length=1000,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Item name'}))

     

    category = forms.ChoiceField(widget=forms.RadioSelect, choices=CATAGORY_CHOICES)

    max_price = forms.DecimalField(label = _('Max Bidding Price'))

    start_price = forms.DecimalField(label = _('Start Bidding Price'))

    increment = forms.DecimalField(label = _('Minmum Bidding Increment'))

    duration = forms.IntegerField(label = _('How do you want this Item on bidding?'),min_value = 3,max_value = 365,
                                    widget = forms.NumberInput({
                                    'class': 'form-control',
                                    'placeholder': '10 (days)'}))


class AddressForm(forms.Form):
    street1 = forms.CharField(label = _('Street1'),max_length=1000,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Street1'}))
    street2 = forms.CharField(label = _('Street2'),max_length=1000,
                              required = False,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Street2'}))
    city = forms.CharField(label = _('City'),max_length=1000,
                              required = False,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'City'}))
    state = forms.CharField(label = _('State'),max_length=1000,
                              required = False,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'State (All lowercase; do pennsylvania not pa'}))
    zipcode = forms.IntegerField(label = _('ZipCode'),min_value = 10000,max_value = 99999,
                                    widget = forms.NumberInput({
                                    'class': 'form-control',
                                    'placeholder': '12345'}))
    email = forms.EmailField()


class PaymentMethodForm(forms.Form):
    cardnumber = forms.CharField(label = _('CardNumber'),max_length=16,min_length=16,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'attrs':{'type':'number'},
                                    'placeholder': '16 digits card number'}))
    cardtype = forms.ChoiceField(label = _('Select Card Type'),
                              widget=forms.RadioSelect, choices=[('1','Visa'),('2','Discover'),('3','Yabe')])


class BuyItemForm(forms.Form):
   quantity = forms.IntegerField(label = _('How many do you want'),min_value = 1,max_value = 99999,
                                    widget = forms.NumberInput({
                                    'class': 'form-control',
                                    'placeholder': '12345'}))
   hasDonate = isVirtual = forms.BooleanField(label = _('Wanna donate $1 For charity?'),
                                    required=False)

class BiddingItemForm(forms.Form):
   howmuch = forms.DecimalField(label = _('My Bidding Price: '))


class RatingForm(forms.Form):
   rating = forms.IntegerField(label = _('Rating: (5 - best vs 1 - worst'),min_value = 1,max_value = 5,
                                    widget = forms.NumberInput({
                                    'class': 'form-control',
                                    'placeholder': 'Rate'}))
   comments = forms.CharField(label = _('Comments:'),max_length=1000,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'I really like this item!'}))





   

