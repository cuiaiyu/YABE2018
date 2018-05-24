"""
Definition of urls for YABE.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = [
    # Examples:
    url(r'^signup/$', app.views.signup, name='signup'),
    url(r'^addItem/$', app.views.addItem, name='addItem'),
    url(r'^addBiddingItem/$', app.views.addBiddingItem, name='addBiddingItem'),
    
    url(r'^addPaymentMethod/$', app.views.addPaymentMethod, name='addPaymentMethod'),
    url(r'^addAddr/$', app.views.addAddr, name='addAddr'),
    url(r'^AddUser/$', app.views.addUser, name='addUser'),
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
                'curruser':'',
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^about', app.views.about, name='about'),
    url(r'^aiyucui-resume/$', app.views.resume, name='resume'),
    url(r'^projects/$', app.views.project, name='project'),
    url(r'^PayBill/(?P<bill>\d+)/$$', app.views.payBill, name='payBill'),
    url(r'^research/(?P<code>\d+)/$$', app.views.research, name='research'),
     url(r'^shipping/(?P<orderIdx>\d+)/(?P<code>(\d+))/$$$', app.views.shipPage, name='shipping'),
    url(r'^sendMessage/$', app.views.sendMessageHandler, name='sendMessage'),
     url(r'^BiddingItemReport/$', app.views.biddingItemReport, name='biddingItemReport'),
    url(r'^Bidding/$', app.views.bidding, name='bidding'),
    url(r'^BiddingHistory/(?P<userType>\d+)/$$', app.views.biddingHistory, name='biddingHistory'),
    url(r'^TeleMarketReport/$', app.views.teleMarketReport, name='teleMarketReport'),
    url(r'^BiddingStat/$', app.views.biddingStat, name='biddingStat'),
    url(r'^Cashback/$', app.views.cashbackHistory, name='cashback'),
    url(r'^transactionHistory/(?P<userType>\d+)/$$', app.views.transactionHistory, name='transactionHistory'),
    url(r'^buyitnow/(?P<itemIdx>\d+)/$$', app.views.buyitnow, name='buyitnow'),
    url(r'^itemPage/(?P<itemIdx>\d+)/$$', app.views.itemPage, name='itemPage'),
    url(r'^LeaveRating/(?P<item_id>\d+)/$$', app.views.addRating, name='leaveRating'),
    
    url(r'^biddingItemPage/(?P<itemIdx>\d+)/$$', app.views.biddingItemPage, name='biddingItemPage'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]# ad
