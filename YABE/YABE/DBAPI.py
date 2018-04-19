from django.db import models
from datetime import datetime
from datetime import timedelta
from operator import attrgetter

import app.models

###################################
# User related functions
###################################

# Create New Users
def user_create(name):
    return app.models.YabeUser.objects.create(yabeusername = str(name),hasMembership = False,isSeller = False,balance = 0)

#------------------------------------------------------------------------------------
# Get all address of a user
# Input: A YabeUser Object
# Output: list of Addr Object, if not addr saved for this result result empty list []
def user_getAllAddr(yabeuser):
    return app.models.Addr.objects.filter(holder = yabeuser)

#------------------------------------------------------------------------------------
# Check whether a user has at least one addr stored
# Input: A YabeUser Object
# Output: True or False
def user_hasAddr(yabeuser):
    return False

#------------------------------------------------------------------------------------
# Create Addr for given user
# Input: balabala
# Output: addr object
def user_createAddr(street1,street2,state,city,zipcode,username):
    user = app.models.YabeUser.objects.get(yabeusername = username)
    return app.models.Addr.objects.create(street1 = street1,
                                            street2 = street2,
                                            city = city,
                                            state = state,
                                            zipcode = zipcode,
                                            holder = user
                                        )

#------------------------------------------------------------------------------------
# Get all payment methods of a user
# Input: A YabeUser Object
# Output: list of payment method Objects, if not payment methods saved for this result result empty list []
def user_getAllPaymentMethod(yabeuser):
    return []

#------------------------------------------------------------------------------------
# Check whether a user has at least one payment methods stored
# Input: A YabeUser Object
# Output: True or False
def user_hasPaymentMethod(yabeuser):
    return False

#------------------------------------------------------------------------------------
# Create Addr for given user
# Input: balabala
# Output: addr object
def user_createPaymentMethod(cardNumber,pType,username):
    user = app.models.YabeUser.objects.get(yabeusername = username)
    return app.models.PaymentMethod.objects.create(cardNumber = cardNumber,
        type = pType,
        holder = user)

#################################
#   Item Related Functions
#################################

def item_create(isVirtual,itemname,category,subcategory,seller,picture,description,quantity,price,isBidding):
    seller_yabe = app.models.YabeUser.objects.get(yabeusername = seller)
    return app.models.Item.objects.create(isVirtual = isVirtual,name = itemname,category = category,subcategory = 0,
                                          seller = seller_yabe,picture = picture,description = description,quantity = quantity,price = price,isBidding = isBidding)

def biddingitem_create(item,maxprice,startprice,increment,duration):
    return app.models.BiddingItem.objects.create(item = item,
                                          max_price = maxprice,
                                          start_price = startprice,
                                          price_increment = increment,
                                          expire_date = datetime.now() + timedelta(days = duration),
                                          isSold = False)

#----------------------------------------------------------------------------
# Given a buyer (yabeuser) object, find all items objects bought by this buyer
# Input: YabeUser object
# Output: list of Order Objects
def item_getByBuyer(buyer):
    # check order objects for the relation 
    # return item objects lIST
    return []

#----------------------------------------------------------------------------
# Given a seller (yabeuser) object, find all item objects sold by this seller
# Input: YabeUser object
# Output: list of Order Objects
def item_getBySeller(seller):
    if seller.isSeller:
        return app.models.Order.objects.get(seller = seller)
    else:
        return []

#----------------------------------------------------------------------------
# check whether a buyer has ever bought a item
# Input: YabeUser object and Item object
# Output: True or False
def item_hasBuyerByItems(buyer,item):
    # check whether a buyer has ever bought the given item, if so, return true
    return False

#-------------------------------------------------------------------------------
# check whether a buyer has ever written a review for an item he or she bought
# Input: YabeUser object and Item object
# Output: True or False
def item_hasBuyerWriteReviewForItems(buyer,item):
    return False


#############################################################
#   Bidding Item related functions
#############################################################

#-------------------------------------------------------------------------------
# Get all bidding Items of a given BUYER
# Input:    A YabeUser Object, 
#           a selector: see below
# Output:   a tuple formed as (List BiddingRecords)
#               if Null Return []
def biddingRecord_getItemByBuyer(yabeuser,selector):
    if selector == 'all':
        #TODO: return all bidding items that the user particiting not matter the status
        return []
    elif selector == 'waiting':
        #TODO: return bidding items as that BiddingRecord.buyer = yabeuser && BiddingRecord.status == "waiting"
        return []
    elif selector == "won":
        #TODO: return biddingItems as that BiddingRecord.buyer = yabeuser && BiddingRecord.status == "won"
        return []
    elif selector == "lost":
        #TODO: return biddingItems as that BiddingRecord.buyer = yabeuser && BiddingRecord.status == "lost"
        return []
    else:
        #ERROR MESSGAE
        return []

#-------------------------------------------------------------------------------
# Get all bidding Items of a given SELLER
# Input:    A YabeUser Object, 
#           a selector "onlyWon": see below
# Output:   a tuple formed as (List of Items Objects, List BiddingItem Objects)
#               if Null Return ([],[])
#           note: in the tuple, Items[i].itemname == Bidding[i].itemname
def biddingRecord_getItemBySeller(yabeuser,selector):
    if selector == 'all':
        #TODO: return all bidding items records that the user sells regardless of the status
        return []
    elif selector == 'sold':
        #TODO: return bidding items records as that BiddingItem.isSold == True
        return []
    elif selector == "waiting":
        #TODO: return biddingItems records as that BiddingItem.isSold == False
        return []
    else:
        #ERROR MESSGAE
        return []

#-------------------------------------------------------------------------------
# Get all bidding records for a given Item
# Input:    A BiddingItem Object
# Output:   A list of BiddingRecord
def biddingRecord_getBuyerByItem(item):
    return []

#--------------------------------------------------------------------------------
def buyItem(item,buyer,seller,quantity,shipfrom,shipto):
    # create transaction:
    myorder = app.models.Order.objects.create(item_id = item,
                                    buyer_id = buyer,
                                    seller_id = seller,
                                    quantity = quantity,
                                    ship_from = shipfrom,
                                    ship_to = shipto,
                                    status = "purchased"
                                    )
    # change item:
    item.quantity = item.quantity-quantity
    item.save()
    buyer.balance = buyer.balance - quantity*item.price
    buyer.save()
    seller.balance = seller.balance + quantity*item.price
    seller.save()
    if buyer.hasMembership == True and item.name != 'YABEDONATION' and item.name != 'YABEVIP':
        app.models.Cashback.objects.create(ammount = quantity*item.price/20,
        order = myorder,
        buyer = buyer)


def bidItem(item,buyer,price,shipfrom,shipto):
    biddingItem = app.models.BiddingItem.objects.get(item = item)
    if price < biddingItem.start_price:
        return 1
    elif price < bid_getHighestPrice(biddingItem) + biddingItem.price_increment:
        return 2
    elif price >= biddingItem.max_price:
        #To buy
        winBidding(item,buyer,price,shipfrom,shipto)
    else:
        app.models.BiddingRecord.objects.create(bid_item = biddingItem,
                                                buyer = buyer,
                                                status = "waiting",
                                                bid_price = price)


def winBidding(item,buyer,price,shipfrom,shipto):
     biddingItem = app.models.BiddingItem.objects.get(item = item)
     myorder = app.models.Order.objects.create(item_id = item,
                                    buyer_id = buyer,
                                    seller_id = item.seller,
                                    quantity = 1,
                                    ship_from = shipfrom,
                                    ship_to = shipto,
                                    status = "purchased"
                                    )
     app.models.BiddingRecord.objects.create(bid_item = biddingItem,
                                                buyer = buyer,
                                                status = "win",
                                                bid_price = price)
     biddingItem.isSold = True
     item.quantity = 0
     item.save()
     biddingItem.save()

     buyer.balance = buyer.balance - price
     item.seller.balance = item.seller.balance + price
     item.seller.save()

     if buyer.hasMembership == True and item.name != 'YABEDONATION' and item.name != 'YABEVIP':
        app.models.Cashback.objects.create(ammount = item.price/20,
        order = myorder,
        buyer = buyer)

     for record in app.models.BiddingRecord.objects.filter(bid_item = biddingItem):
        if record.buyer != buyer:
            record.status = "lost"
            record.save();


def bid_getHighestPrice(biddingItem):
    records = app.models.BiddingRecord.objects.filter(bid_item = biddingItem)
    if not records:
        return biddingItem.start_price
    return max(records, key=attrgetter('bid_price')).bid_price







