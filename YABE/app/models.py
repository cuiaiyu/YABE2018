"""
Definition of models.
"""

from django.db import models

# User table, which stores specific user meta data
class YabeUser(models.Model):
    yabeusername = models.CharField(max_length = 10,primary_key = True)
    #email = models.EmailField()
    hasMembership = models.BooleanField()
    isSeller = models.BooleanField(default = False)
    balance = models.DecimalField(max_digits = 10,decimal_places = 2)
   
# Item table, which stores every items
class Item(models.Model):
    isVirtual = models.BooleanField(default = False)
    isBidding = models.BooleanField(default = False)
    name = models.CharField(max_length = 20)
    category = models.CharField(max_length = 20)
    subcategory = models.CharField(max_length = 20)
    seller = models.ForeignKey(YabeUser)
    picture = models.ImageField()
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
    #email = models.EmailField()
    holder = models.ForeignKey(YabeUser,on_delete = models.CASCADE)

class Order(models.Model):
    buyer_id = models.ForeignKey(YabeUser,related_name="buyerid")
    seller_id = models.ForeignKey(YabeUser, related_name="sellerid",)
    item_id = models.ForeignKey(Item)
    ship_from = models.ForeignKey(Addr,related_name="fromAddr")
    ship_to = models.ForeignKey(Addr,related_name="toAddr")
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









# Create your models here.
