"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime,timedelta
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
from YABE.settings import MEDIA_ROOT

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
import os




def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    print('render home')
    YABEinitialize(request)
    print('YABE is initalized')
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

def teleMarketReport(request):
    '''Rends Project Page'''
    curruser = request.user.username
    #user = app.models.YabeUser.objects.get(yabeusername = curruser)
    users = list(app.models.YabeUser.objects.all())
    userlist = []
    cnt = 0;
    for user in users:
        curruser = {'name':user.yabeusername,
                    'annualIncome':user.annualIncome,
                    'gender':user.gender,
                    'age':user.age,
                    'email':'',
                    'totalBidding':len(list(app.models.BiddingRecord.objects.filter(buyer = user,bidding_date__gt = datetime.now()-timedelta(days = 7)))),
                    'wonBidding':len(list(app.models.BiddingRecord.objects.filter(buyer = user,status = 'Win',bidding_date__gt = datetime.now()-timedelta(days = 7)))),
                    'addr':''
                    }
        email = "N/A"
        if list(app.models.Addr.objects.filter(holder = user)) != []:
            address = list(app.models.Addr.objects.filter(holder = user))[0]
            email = address.email
            addr = "".join([address.city,', ',address.state])
        curruser['email'] = email
        curruser['addr'] = addr
        userlist.append(curruser)
    return render(
        request,
         'app/TeleMarketReport.html',
        context = 
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'curr_selection':'',#curr_selection,
            'curruser':request.user.username,
            'users':userlist
        }
    )

def biddingStat(request):
    '''Rends Project Page'''
    curruser = request.user.username
    #user = app.models.YabeUser.objects.get(yabeusername = curruser)
    biddingitems = list(app.models.BiddingItem.objects.all())
    CATAGORY_CHOICES = [('1','Bookstore'),('2','Collectibles & Art'),
               ('3','Electronic'),('4','Fashion'),
               ('5','Home & Garden'),('6','Sporting Goods'),
               ('7','Toys & Hobbies'),('8','Others')]
    catas = []
    for i in range(0,8):
        cata = {
            'name': CATAGORY_CHOICES[i][1],
            'availableItem':len([j for j in list(app.models.BiddingItem.objects.filter(expire_date__gt = datetime.now())) if j.item.category == CATAGORY_CHOICES[i][1]]),
            'totalBidding': len([j for j in list(app.models.BiddingRecord.objects.filter(bidding_date__gt = datetime.now() - timedelta(days = 7))) if j.bid_item.item.category == CATAGORY_CHOICES[i][1]]),
            }
        catas.append(cata)


    return render(
        request,
         'app/BiddingStat.html',
        context = 
        {
            'host_info':BasicData.HOST,
            'year':datetime.now().year,
            'curr_selection':'',#curr_selection,
            'curruser':request.user.username,
            'catas':catas
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
            if buyer.balance < -100:
                return redirect('research',code = 12)
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
            order = DBAPI.buyItem(item = item, buyer = buyer_id,seller = seller_id,quantity = quant, shipfrom = shipfrom, shipto=shipto)
            if wannaDonate:
                donation = app.models.Item.objects.get(name = 'YABEDONATION',seller = app.models.YabeUser.objects.get(yabeusername = 'YABEADMIN'))
                donator = donation.seller
                DBAPI.buyItem(item = donation, 
                              buyer = buyer_id,seller = donator,quantity = 1, shipfrom = shipfrom, shipto=shipto)
            return redirect('shipping',orderIdx = order.id, code=1)
    else:
        form = app.forms.BuyItemForm()
        form.quantity = forms.IntegerField(label = _('How many do you want'),min_value = 1,max_value = item.quantity,
                                    widget = forms.NumberInput({
                                    'class': 'form-control',
                                    'placeholder': ['max = ',str(item.quantity)],}))
    buyer = app.models.YabeUser.objects.get(yabeusername = request.user.username)
    hasBought = (list(app.models.Order.objects.filter(buyer_id = buyer,item_id = item)) != [])
    comments = list(app.models.Review.objects.filter(buyer = buyer,item = item))
    hasCommented = (comments == [])
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
            if buyer.balance < -100:
                 return redirect('research',code = 12)
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
            elif code == 4:
                a = 1
            else:
                return redirect('shipping',orderIdx = code.id, code = 1)
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
def shipping(request,orderIdx,code):
    code = str(code)
    user = app.models.YabeUser.objects.get(yabeusername = request.user.username)
    order = app.models.Order.objects.get(id = orderIdx)
    addr = app.models.Addr.objects.filter(holder = user)[0]
    message = ""
    if code == '1':
        address = ''.join([addr.street1,', ', addr.city, ',', addr.state, ', ', addr.zipcode])
        massage = ''
        if not order.item_id.isVirtual:
            if user.hasMembership:
                message = ''.join(['Purchase successfully! Free ship to your address: ',address])
            else:
                message = ''.join(['Purchase successfully! Ship with $10 to your address: ',address])
                adminseller = app.models.YabeUser.objects.get(yabeusername = 'YABEADMIN')
                shiporder = DBAPI.buyItem(buyer = user,
                                                seller = adminseller,
                                                item = app.models.Item.objects.get(name = 'YABESHIPPING',seller=adminseller),
                                                shipfrom = app.models.Addr.objects.filter(holder = adminseller)[0],
                                                shipto = addr,
                                                quantity = 1)
                shiporder.status = 'Shipped'
                shiporder.save()
        else:
            message = ''.join(['Purchase succefully! Your item will be delivered to your email: ', addr.email])
    elif code == '2':
        order.status = "Shipped"
        order.save()
        message = "Shipping successfully!"

    return message

def shipPage(request,orderIdx,code):
    """Renders the resume page."""
    return render(
        request,
        'app/research.html',
        context = 
        {
            'year':datetime.now().year,            
            'curruser':request.user.username,
            'message':shipping(request,orderIdx,code),
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
        vip = app.models.Item.objects.get(name = 'YABEVIP',seller = app.models.YabeUser.objects.get(yabeusername = 'YABEADMIN'))
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
    elif code == '11':
         message = "You bought this product successfully!"
    elif code == '12':
        message = "You account seems overdue $100. Please check your balance before you take any operation. :-)"
    elif code == '13':
        yabeUser = app.models.YabeUser.objects.get(yabeusername = request.user.username)
        cashback = 0
        cashbacklist = list(app.models.Cashback.objects.filter(buyer = yabeUser))
        for cb in cashbacklist:
            cashback = cashback + cb.ammount
            cb.delete()
        yabeUser.balance = yabeUser.balance + cashback
        yabeUser.save()
        message = "".join(['You save cashback $', str(cashback), ' to your account'])

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

def payBill(request,bill):
    """Renders the resume page."""
    yabeUser = app.models.YabeUser.objects.get(yabeusername = request.user.username)
    pml = list(app.models.PaymentMethod.objects.filter(holder = yabeUser))
    if pml == []:
        return redirect('research',code = 7)
    pm = pml[0]
    yabeUser.balance = yabeUser.balance + int(bill);
    yabeUser.save()
    message = "".join(['You successfully save $',str(bill),' to your account from your card: ', str(pm.cardNumber),'!'])
    return render(
        request,
        'app/PayBill.html',
        context = 
        {
            'year':datetime.now().year,            
            'curruser':request.user.username,
            'message':message,
        }
    )

def buyitnow(request,itemIdx):
    """Renders the resume page."""
    item = app.models.Item.objects.get(id = itemIdx)
    biddingItem = app.models.BiddingItem.objects.get(item = item)
    buyer = app.models.YabeUser.objects.get(yabeusername = request.user.username)

    if request.user.username == '':
        return redirect('research',code = 9)
    if buyer.balance < -100:
        return redirect('research',code = 12)
   
    
    order = DBAPI.winBidding(item = item,
               buyer = buyer,
               price = biddingItem.max_price,
               shipfrom = DBAPI.user_getAllAddr(item.seller)[0],
               shipto = DBAPI.user_getAllAddr(buyer)[0])
    shipMsg = shipping(request,order.id,1)
    message = ''.join(['You Bought the bidding item ',item.name,' now! ',shipMsg])
    
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
            DBAPI.user_create(username,gender = 'Male', age = 10, annualIncome = '<50,000')
            login(request, user) # login in defined in this page
            return redirect('addUser')

    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form},)

# Add A Product
def addItem(request):
    if request.method == 'POST':
        form = app.forms.AddItemForm(request.POST,request.FILES)
        if form.is_valid():
            itemname = form.cleaned_data.get('itemname')
            quantity = form.cleaned_data.get('quantity')
            isVirtual = form.cleaned_data.get('isVirtual')
            pic = form.cleaned_data['picture']
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            print('pic:')
            print(pic)
            print('show pic')
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
        form = app.forms.AddBiddingItemForm(request.POST,request.FILES)
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
            email = str(form.cleaned_data.get('email'))
            username = request.user.username;
            curraddr = list(app.models.Addr.objects.filter(holder = app.models.YabeUser.objects.get(yabeusername = request.user.username)))
            if curraddr == []:
                app.models.Addr.objects.create(street1 = street1,street2=street2,state = state,city = city,zipcode = zipcode,
                                               holder = app.models.YabeUser.objects.get(yabeusername = request.user.username),
                                               email = email)
            else:
                addr =  app.models.Addr.objects.get(holder = app.models.YabeUser.objects.get(yabeusername = request.user.username))
                addr.street1 = street1
                addr.street2 = street2
                addr.state = state
                addr.city = city
                addr.email = email
                addr.zipcode = zipcode
                addr.save()

            return redirect('research', code = 4)

    else:
        form = app.forms.AddressForm()
    return render(request, 'app/addAddr.html', {'form': form})

def addUser(request):
    username = request.user.username;
    user = app.models.YabeUser.objects.get(yabeusername = username)
    if request.method == 'POST':
        form = app.forms.AddUserForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data.get('gender')
            if str(gender) == '1':
                gender = 'Male'
            else:
                gender = 'Female'
            INCOME_CHOICES = [('1','<50,000'),('2','50,000-100,000'),('3','100,000-200,000'),('4','>200,000')]
            user.age = form.cleaned_data.get('age')
            incomeIdx = int(form.cleaned_data.get('annualIncome'))-1
            user.gender = gender;
            user.annualIncome = INCOME_CHOICES[incomeIdx][1]
            user.save()
            return redirect('home')

    else:
        form = app.forms.AddUserForm()
    return render(request, 'app/AddUser.html', {'form': form})



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
            curraddr = list(app.models.PaymentMethod.objects.filter(holder = app.models.YabeUser.objects.get(yabeusername = request.user.username)))
            if curraddr == []:
                DBAPI.user_createPaymentMethod(cardNumber = cardNumber,pType = type,username = username)
            else:
                pm = app.models.PaymentMethod.objects.get(holder = app.models.YabeUser.objects.get(yabeusername = request.user.username))
                pm.cardNumber = cardNumber
                pm.type = type
                pm.save()
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

def YABEinitialize(request):
    # Create admin user YABE if not existing
    if list(app.models.YabeUser.objects.filter(yabeusername = 'YABEADMIN')) == []:
        yabe = app.models.YabeUser.objects.create(yabeusername = 'YABEADMIN',
                                           hasMembership = True,
                                           isSeller = True,
                                           balance = 0,
                                           age = 100,
                                           annualIncome = '',
                                           gender = 'Male'
                                           )    
    yabe = app.models.YabeUser.objects.get(yabeusername = 'YABEADMIN')
    if list(app.models.Addr.objects.filter(holder = yabe)) == []:
        app.models.Addr.objects.create(street1 = 'YABE',
                                        city = 'YABE',
                                        state = 'YABE',
                                        zipcode = 11111,
                                        holder = yabe
                                        )
    if list(app.models.PaymentMethod.objects.filter(holder = yabe)) == []:
        app.models.PaymentMethod.objects.create(cardNumber = '1111222233334444',
                                                type = 'YABE',
                                                holder = yabe)
    # Create YABEDONATION, YABEVIP,YABESHIPPING
    if list(app.models.Item.objects.filter(seller = yabe,name = 'YABEDONATION')) == []:
        app.models.Item.objects.create(name = 'YABEDONATION',
                                       category = 'YABE',
                                       subcategory = 'YABE',
                                       seller = yabe,
                                       description = '',
                                       isVirtual = True,
                                       quantity = 99999,
                                       price = 1)
    if list(app.models.Item.objects.filter(seller = yabe,name = 'YABEVIP')) == []:
        app.models.Item.objects.create(name = 'YABEVIP',
                                       category = 'YABE',
                                       subcategory = 'YABE',
                                       seller = yabe,
                                       description = '',
                                       quantity = 99999,
                                       isVirtual = True,
                                       price = 100)
    if list(app.models.Item.objects.filter(seller = yabe,name = 'YABESHIPPING')) == []:
        app.models.Item.objects.create(name = 'YABESHIPPING',
                                        category = 'YABE',
                                        subcategory = 'YABE',
                                        seller = yabe,
                                        description = '',
                                        quantity = 99999,
                                        isVirtual = True,
                                        price = 10)
    biddings = list(app.models.BiddingItem.objects.filter(isSold = False,
                                                          expire_date__lt = datetime.now()))
    for bid in biddings:
        records = list(app.models.BiddingRecord.objects.filter(bid_item = bid))
        maxbid = records[0]
        for r in records:
            if r.bid_price > maxbid.bid_price:
                maxbid = r
        order = DBAPI.winBidding(item = bid.item,
                         buyer = maxbid.buyer,
                         price = maxbid.price,
                         shipfrom = list(app.models.Addr.objects.filter(holder = bid.item.seller))[0],
                         shipto = list(app.models.Addr.objects.filter(holder = maxbid.buyer))[0])
        maxbid.delete()
        shipping(request,order.id,1)
        

       



    return []








