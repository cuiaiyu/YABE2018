"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import smtplib
from django.core.serializers import json
from YABE import BasicData
from YABE import ProjectData
from YABE import DBAPI
import app.forms
from django.db import models
import app.models
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail
import json
import smtplib
from email.mime.text import MIMEText

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms




def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    print('render home')
    print(request.user)
    print(type(request.user))
    return render(
        request,
        'app/index.html',
        context = {
            'host_info':BasicData.HOST,
            'projectForm':ProjectData.getRecentThreeProjects(),
            'year':datetime.now().year,
            'curruser':request.user.username,
        }

        
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context =
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'curruser':request.user.username,
        }
    )


def about(request):

    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    username = request.user.username
    yabeUser = app.models.YabeUser.objects.get(yabeusername = username)
    print(yabeUser.isSeller)
    print('!!!')
    cashback = 0
    cashbacklist = list(app.models.Cashback.objects.filter(buyer = yabeUser))
    for cb in cashbacklist:
        cashback = cashback + cb.ammount

    return render(
        request,
        'app/about.html',
        context =
        {
            'year':datetime.now().year,
            'host_info':BasicData.HOST,
            'curruser':request.user.username,
            'cards': app.models.PaymentMethod.objects.filter(holder = yabeUser),
            'address':DBAPI.user_getAllAddr(yabeUser),
            'yabeuser':yabeUser,
            'cashback':cashback,
        }
    )

def resume(request):
    """Renders the resume page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/aiyucui-resume.html',
        context=
        {
            'title':'resume',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'curruser':request.user.username,
        }
    )


def project(request):
    '''Rends Project Page'''
    assert isinstance(request, HttpRequest)
    value=request.GET.get("category");
    search_query = request.GET.get('search_box')
    if search_query != None:
        items = list(app.models.Item.objects.filter(name__contains=search_query,quantity__gt = 0,isBidding = False))
    else:
        print(value)
        print('!!!here we ho')
        search_content = request.GET.get("searchContent")
        print(search_content)
        #key=request.GET.get("key")
        if value==None or value == 0:
            items = list(app.models.Item.objects.filter(quantity__gt = 0,isBidding = False));
        else:
            items = list(app.models.Item.objects.filter(category=value,quantity__gt = 0,isBidding = False));
    
    
    return render(
        request,
         'app/Products.html',
        context = 
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'projectForm':'',#projectForm,
            'products':items,
            'yearList':ProjectData.getValueListByAttr('year'),
            'categoryList':ProjectData.getValueListByAttr('category'),
            'curr_selection':'',#curr_selection,
            'curruser':request.user.username,
        }
    )

def transactionHistory(request,userType):
    '''Rends Project Page'''
    curruser = request.user.username
    user = app.models.YabeUser.objects.get(yabeusername = curruser)
    if str(userType) == "1":
        myorders = list(app.models.Order.objects.filter(buyer_id = user))
    else:
        myorders = list(app.models.Order.objects.filter(seller_id = user))
    return render(
        request,
         'app/TransactionHistory.html',
        context = 
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'curr_selection':'',#curr_selection,
            'curruser':request.user.username,
            'myorders':myorders,
        }
    )
def cashbackHistory(request):
    '''Rends Project Page'''
    curruser = request.user.username
    user = app.models.YabeUser.objects.get(yabeusername = curruser)
    cashbacklist = list(app.models.Cashback.objects.filter(buyer = user))

    return render(
        request,
         'app/Cashback.html',
        context = 
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'curr_selection':'',#curr_selection,
            'curruser':request.user.username,
            'cashbacklist':cashbacklist,
        }
    )
def biddingHistory(request):
    '''Rends Project Page'''
    curruser = request.user.username
    user = app.models.YabeUser.objects.get(yabeusername = curruser)
    mybiddings = list(app.models.BiddingRecord.objects.filter(buyer = user))
    return render(
        request,
         'BiddingHistory.html',
        context = 
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'curr_selection':'',#curr_selection,
            'curruser':request.user.username,
            'mybiddings':mybiddings,
        }
    )
def bidding(request):
    '''Rends Project Page'''
    assert isinstance(request, HttpRequest)
    value=request.GET.get("category");
    search_query = request.GET.get('search_box')
    if search_query != None:
        items = list(app.models.Item.objects.filter(name__contains=search_query,quantity__gt = 0,isBidding = True))
    else:
        print(value)
        print('!!!here we ho')
        search_content = request.GET.get("searchContent")
        print(search_content)
        #key=request.GET.get("key")
        if value==None or value == 0:
            items = list(app.models.Item.objects.filter(quantity__gt = 0,isBidding = True));
        else:
            items = list(app.models.Item.objects.filter(category=value,quantity__gt = 0,isBidding = True));

    return render(
        request,
         'app/Bidding.html',
        context = 
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'projectForm':'',#projectForm,
            'products':items,
            'yearList':ProjectData.getValueListByAttr('year'),
            'categoryList':ProjectData.getValueListByAttr('category'),
            'curr_selection':'',#curr_selection,
            'curruser':request.user.username,
        }
    )

def itemPage(request,itemIdx):
    '''Rends Project Page'''
    if request.user.username == '':
        return redirect('research',code = 9)
    buyer = app.models.YabeUser.objects.get(yabeusername = request.user.username)
    item = app.models.Item.objects.get(id = itemIdx);
    if request.method == 'POST':
        form = app.forms.BuyItemForm(request.POST)
        form.quantity = forms.IntegerField(label = _('How many do you want'),min_value = 1,max_value = item.quantity,
                                    widget = forms.NumberInput({
                                    'class': 'form-control',
                                    'placeholder': ['max = ',str(item.quantity)],}))
        if form.is_valid():
            if list(app.models.Addr.objects.filter(holder = buyer)) == []:
                return redirect('research',code = 6)
            if list(app.models.PaymentMethod.objects.filter(holder = buyer)) == []:
                return redirect('research',code = 7)
            quant = form.cleaned_data.get('quantity')
            wannaDonate =  form.cleaned_data.get('hasDonate')
            buyer_id = app.models.YabeUser.objects.get(yabeusername = request.user.username)
            seller_id = item.seller
            shipfrom = DBAPI.user_getAllAddr(seller_id)[0]
            shipto = DBAPI.user_getAllAddr(buyer_id)[0]
            if quant > item.quantity:
                return redirect('research',code = 10)
            DBAPI.buyItem(item = item, buyer = buyer_id,seller = seller_id,quantity = quant, shipfrom = shipfrom, shipto=shipto)
            if wannaDonate:
                donation = app.models.Item.objects.get(name = 'YABEDONATION')
                donator = donation.seller
                DBAPI.buyItem(item = donation, 
                              buyer = buyer_id,seller = donator,quantity = 1, shipfrom = shipfrom, shipto=shipto)
    else:
        form = app.forms.BuyItemForm()
        form.quantity = forms.IntegerField(label = _('How many do you want'),min_value = 1,max_value = item.quantity,
                                    widget = forms.NumberInput({
                                    'class': 'form-control',
                                    'placeholder': ['max = ',str(item.quantity)],}))
    buyer = app.models.YabeUser.objects.get(yabeusername = request.user.username)
    hasBought = (list(app.models.Order.objects.filter(buyer_id = buyer,item_id = item)) != [])
    print(hasBought)
    comments = list(app.models.Review.objects.filter(buyer = buyer,item = item))
    print(comments)
    print('hhhhhhhhhhhh')
    hasCommented = (comments == [])
    (print(hasCommented))
    return render(
        request,
         'app/ItemPage.html',
        context = 
        {
            'form':form,
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'item':item,
            'curruser':request.user.username,
            'quantityList':range(1,item.quantity+1),
            'hasBought':hasBought and hasCommented,
            'reviews':comments
        }
    )
        
def biddingItemPage(request,itemIdx):
    '''Rends Project Page'''
    if request.user.username == '':
        return redirect('research',code = 9)
    buyer = app.models.YabeUser.objects.get(yabeusername = request.user.username)
    item = app.models.Item.objects.get(id = itemIdx);
    biddingItem = app.models.BiddingItem.objects.get(item = item)

    if request.method == 'POST':
        form = app.forms.BiddingItemForm(request.POST)
        if form.is_valid():
            if list(app.models.Addr.objects.filter(holder = buyer)) == []:
                return redirect('research',code = 6)
            if list(app.models.PaymentMethod.objects.filter(holder = buyer)) == []:
                return redirect('research',code = 7)
            howmuch = form.cleaned_data.get('howmuch')
            buyer_id = app.models.YabeUser.objects.get(yabeusername = request.user.username)
            #if (app.models.BiddingRecord.objects.get(buyer = buyer_id) != None):
            #    return redirect('research',code = 3)
            seller_id = item.seller
            shipfrom = DBAPI.user_getAllAddr(seller_id)[0]
            shipto = DBAPI.user_getAllAddr(buyer_id)[0]
            code = DBAPI.bidItem(item = item, buyer = buyer_id, shipfrom = shipfrom, shipto=shipto,price = howmuch)
            if code == 1:
                 return redirect('research',code = 1)
            elif code == 2:
                 return redirect('research', code = 2)

    else:
        form = app.forms.BiddingItemForm()

    curr_price = DBAPI.bid_getHighestPrice(biddingItem)
    if curr_price == -1:
        curr_price = biddingItem.start_price
    records = app.models.BiddingRecord.objects.filter(bid_item = biddingItem)
    return render(
        request,
         'app/BiddingItemPage.html',
        context = 
        {
            'form':form,
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'item':item,
            'biddingitem':biddingItem,
            'curr_price':curr_price,
            'curruser':request.user.username,
            'quantityList':range(1,item.quantity+1),
            'biddingHistory':records,
        }
    )
        
        

def research(request,code):
    """Renders the resume page."""
    massage = ''
    code = str(code)
    print("in research: code")
    print(code)
    if code == "1":
        message = "Your price is too low to participate in bidding! :)"
    elif code == "2":
        message = "Not meet minimum bidding increment!"
    elif code == "3":
        message = "You already bidded this item!"
    elif code == "4":
        message = "Adding Successfully!!"
    elif code == "5":
        curruser = app.models.YabeUser.objects.get(yabeusername = request.user.username);
        if list(app.models.Addr.objects.filter(holder = curruser)) == []:
                return redirect('research',code = 6)
        if list(app.models.PaymentMethod.objects.filter(holder = curruser)) == []:
                return redirect('research',code = 7)
        
        curruser.isSeller = True
        curruser.save()
        message = "You are a seller now!!"
    elif code == "6":
        message = "You do not a address!!"
    elif code == "7":
        message = "You do not a payment method!!"
    elif code == "8":
        curruser = app.models.YabeUser.objects.get(yabeusername = request.user.username);
        if list(app.models.Addr.objects.filter(holder = curruser)) == []:
                return redirect('research',code = 6)
        if list(app.models.PaymentMethod.objects.filter(holder = curruser)) == []:
                return redirect('research',code = 7)
        vip = app.models.Item.objects.get(name = 'YABEVIP')
        us = vip.seller
        shipfrom = DBAPI.user_getAllAddr(us)[0]
        shipto = DBAPI.user_getAllAddr(curruser)[0]
        DBAPI.buyItem(item = vip, 
                    buyer = curruser,seller = us,quantity = 1, shipfrom = shipfrom, shipto=shipto)
        curruser.hasMembership = True
        curruser.save()
        message = "You are a VIP now!!"
    elif code == "9":
         message = "Please log in to access more features!"
    elif code == "10":
         message = "Your quantity exceed the maximum in stock!"

    return render(
        request,
        'app/research.html',
        context = 
        {
            'year':datetime.now().year,            
            'curruser':request.user.username,
            'message':message,
        }
    )

def buyitnow(request,itemIdx):
    """Renders the resume page."""
    if request.user.username == '':
        return redirect('research',code = 9)
   
    item = app.models.Item.objects.get(id = itemIdx)
    biddingItem = app.models.BiddingItem.objects.get(item = item)
    buyer = app.models.YabeUser.objects.get(yabeusername = request.user.username)
    DBAPI.winBidding(item = item,
               buyer = buyer,
               price = biddingItem.max_price,
               shipfrom = DBAPI.user_getAllAddr(item.seller)[0],
               shipto = DBAPI.user_getAllAddr(buyer)[0])
    message = ['You Bought item',item.name,' now!']

    return render(
        request,
        'app/BuyItNow.html',
        context = 
        {
            'year':datetime.now().year,            
            'curruser':request.user.username,
            'message':message,
        }
    )


def sendMessageHandler(request):
    """Renders the resume page."""
    assert isinstance(request, HttpRequest)
    
    #Get data from browser
   
    name=request.GET.get("name")
    FROM=request.GET.get("email")
    subject=request.GET.get("subject")
    content=request.GET.get("content")
    
    

    #Return
    return render(request,
     'app/thxSendMsg.html',
        context = 
        {
            'year':datetime.now().year,
            'status':'Sorry, this method is still in developing.',
            'curruser':request.user.username,           
        }
    )

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(type(request.user))
            DBAPI.user_create(username)
            login(request, user) # login in defined in this page
            return redirect('home')

    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form},)

# Add A Product
def addItem(request):
    if request.method == 'POST':
        form = app.forms.AddItemForm(request.POST)
        if form.is_valid():
            itemname = form.cleaned_data.get('itemname')
            quantity = form.cleaned_data.get('quantity')
            isVirtual = form.cleaned_data.get('isVirtual')
            pic = form.cleaned_data.get('picture')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            
            price = form.cleaned_data.get('price')

            # add item to DB
            DBAPI.item_create(itemname = itemname,quantity = quantity,isVirtual = isVirtual,
                              picture = pic,description = description,category = int(category),subcategory = 0,
                              seller = request.user.username,
                              price = price,
                              isBidding = False)

           #login(request, user) # login in defined in this page
            return redirect('research', code = 4)

    else:
        form = app.forms.AddItemForm()
    return render(request, 'app/addItem.html', context = 
        {
            'form': form,
            'year':datetime.now().year,
            'status':'Sorry, this method is still in developing.',
            'curruser':request.user.username,           
        })


# Add A Bidding Product
def addBiddingItem(request):
    if request.method == 'POST':
        form = app.forms.AddBiddingItemForm(request.POST)
        if form.is_valid():
            itemname = form.cleaned_data.get('itemname')
            isVirtual = form.cleaned_data.get('isVirtual')
            pic = form.cleaned_data.get('picture')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            maxprice = form.cleaned_data.get('max_price')
            increment = form.cleaned_data.get('increment')
            startprice = form.cleaned_data.get('start_price')
            duration = form.cleaned_data.get('duration')
            # add item to DB
            myitem = DBAPI.item_create(itemname = itemname,quantity = 1,isVirtual = isVirtual,
                              picture = pic,description = description,category = int(category),subcategory = 0,
                              seller = request.user.username,isBidding = True,price = startprice)
            
           
            DBAPI.biddingitem_create(item = myitem,maxprice = maxprice,startprice=startprice,increment=increment,duration = duration)
            return redirect('research', code = 4)

    else:
        form = app.forms.AddBiddingItemForm()
    return render(request, 'app/addBiddingItem.html', {'form': form},)


def addAddr(request):
    if request.method == 'POST':
        form = app.forms.AddressForm(request.POST)
        if form.is_valid():
            street1 = form.cleaned_data.get('street1')
            street2 = form.cleaned_data.get('street2')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zipcode = str(form.cleaned_data.get('zipcode'))
            username = request.user.username;
            DBAPI.user_createAddr(street1 = street1,street2=street2,state = state,city = city,zipcode = zipcode,username = username)
            return redirect('research', code = 4)

    else:
        form = app.forms.AddressForm()
    return render(request, 'app/addAddr.html', {'form': form})


def addPaymentMethod(request):
    if request.method == 'POST':
        form = app.forms.PaymentMethodForm(request.POST)
        if form.is_valid():
            cardNumber = form.cleaned_data.get('cardnumber')
            cardtype = form.cleaned_data.get('cardtype')
            print('cardtype')
            print(cardtype)                                
            if cardtype == '1':
                type = 'Visa'
            elif cardtype == '2':
                type = 'Discover'
            else:
                type = 'Yabe'
            username = request.user.username;
            DBAPI.user_createPaymentMethod(cardNumber = cardNumber,pType = type,username = username)
            return redirect('research', code = 4)

    else:
        form = app.forms.PaymentMethodForm()
    return render(request, 'app/addPaymentMethod.html', {'form': form})

def addRating(request,item_id):
    if request.method == 'POST':
        form = app.forms.RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data.get('rating')
            comments = str(form.cleaned_data.get('comments'))
            username = request.user.username;
            user = app.models.YabeUser.objects.get(yabeusername = username)
            item = app.models.Item.objects.get(id = item_id)
            app.models.Review.objects.create(feedback = comments, buyer = user, item = item,rating = rating )
            return redirect('itemPage', itemIdx = item_id)

    else:
        form = app.forms.RatingForm()
    return render(request, 'app/leaveRating.html', {'form': form})







