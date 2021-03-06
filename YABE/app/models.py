"""
Definition of models.
"""

from django.db import models
from django.core.files.storage import FileSystemStorage

#fs = FileSystemStorage(location='data/')

# User table, which stores specific user meta data
class YabeUser(models.Model):
    yabeusername = models.CharField(max_length = 10,primary_key = True)
    #email = models.EmailField()
    hasMembership = models.BooleanField()
    age = models.IntegerField()
    gender = models.CharField(max_length = 10)
    annualIncome = models.CharField(max_length = 20)
    isSeller = models.BooleanField(default = False)
    balance = models.DecimalField(max_digits = 10,decimal_places = 2)
   
# Item table, which stores every items
class Item(models.Model):
    isVirtual = models.BooleanField(default = False)
    isBidding = models.BooleanField(default = False)
    name = models.CharField(max_length = 20)
    category = models.CharField(max_length = 20)
    subcategory = models.CharField(max_length = 20)
    seller = models.ForeignKey(YabeUser,on_delete=models.DO_NOTHING)
    picture = models.ImageField(default = 'static/app/images/YABE.png')
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits = 10,decimal_places = 2)



# BiddingItem, stores information of biddingItem other than a regular item
class BiddingItem(models.Model):
    item = models.ForeignKey(Item,on_delete = models.CASCADE)
    max_price = models.DecimalField(max_digits = 10,decimal_places = 2)
    start_price = models.DecimalField(max_digits = 10,decimal_places = 2)
    price_increment = models.DecimalField(max_digits = 10,decimal_places = 2)
    isSold = models.BooleanField(default = False)
    expire_date = models.DateTimeField()


# For a certain biddingItem, store the bidding prices
class BiddingRecord(models.Model):
    bid_item = models.ForeignKey(BiddingItem, on_delete = models.CASCADE)
    buyer = models.ForeignKey(YabeUser, on_delete = models.CASCADE)
    bidding_date = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 7) # the bidding status ['waiting","won","lost"]
    bid_price = models.DecimalField(max_digits = 10,decimal_places = 2)

# Addr of each user
class Addr(models.Model):
    street1 = models.CharField(max_length = 100)
    street2 = models.CharField(max_length = 100, null = True)
    city = models.CharField(max_length = 20)
    state = models.CharField(max_length = 15)
    zipcode = models.CharField(max_length = 5)
    email = models.EmailField(default = 'yabe@yabe.com')
    holder = models.ForeignKey(YabeUser,on_delete = models.CASCADE)

class Order(models.Model):
    buyer_id = models.ForeignKey(YabeUser,related_name="buyerid",on_delete=models.DO_NOTHING)
    seller_id = models.ForeignKey(YabeUser, related_name="sellerid",on_delete=models.DO_NOTHING)
    item_id = models.ForeignKey(Item,on_delete=models.DO_NOTHING)
    ship_from = models.ForeignKey(Addr,related_name="fromAddr",on_delete=models.DO_NOTHING)
    ship_to = models.ForeignKey(Addr,related_name="toAddr",on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    status = models.TextField()
    datetime = models.DateTimeField(auto_now = True)

class PaymentMethod(models.Model):
    cardNumber = models.CharField(max_length = 16)
    type = models.CharField(max_length = 10)
    holder = models.ForeignKey(YabeUser,on_delete = models.CASCADE)
    
class Review(models.Model):
    feedback = models.TextField()
    datetime = models.DateTimeField(auto_now = True)
    rating = models.IntegerField()
    item = models.ForeignKey(Item,on_delete = models.CASCADE)
    buyer = models.ForeignKey(YabeUser,on_delete = models.CASCADE)

 
class Cashback(models.Model):
    ammount = models.DecimalField(max_digits = 10,decimal_places = 2)
    order = models.ForeignKey(Order,on_delete = models.DO_NOTHING)
    buyer = models.ForeignKey(YabeUser,on_delete = models.DO_NOTHING)









# Create your models here.
