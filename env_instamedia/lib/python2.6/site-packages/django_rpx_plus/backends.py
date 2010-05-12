from django.conf import settings
from django.contrib.auth.models import User
#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
from django.utils.http import urlencode
from django.utils import simplejson

from django_rpx_plus.models import RpxData

import urllib2

RPX_API_AUTH_URL = 'https://rpxnow.com/api/v2/auth_info'

class RpxBackend:
    def get_user(self, user_id): #required to have get_user method.
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, token):
        '''
        Called by views.rpx_response. Takes a token (a hash that was sent by
        RPX when user logged in through the service) and uses it to query 
        RPX's auth_info API to verify that the user logged in successfully and
        to get additional user data (the user's profile). Then returns a User
        object if the RPX login is associated to one (considered successful
        authentication), returns a RpxData object if the RPX login is NOT
        associated to any User object (the user needs to register), or returns
        None if unsuccessful RPX login.

        @type token: string
        @param token: RPX provided hash used for auth_info API call.
        @return: User obj if successful login and user is registered.
                 RpxData obj if successful login but user is NOT registered.
                 None if error.
        '''
        #As detailed on https://rpxnow.com/docs#api, we send query RPX's API
        #URL to obtain auth_info.
        args = {
            'format': 'json',
            'apiKey': settings.RPXNOW_API_KEY,
            'token': token, #only valid for 10 min
        }
        #Send and get data from RPX API:
        try:
            response = urllib2.urlopen(url = RPX_API_AUTH_URL, data = urlencode(args))
        except urllib2.URLError:
            #Means we couldn't open the url for some reason.
            #TODO: Provide good error message.
            return None

        #Parse the JSON response:
        try:
            response = simplejson.load(response)
        except ValueError:
            #JSON couldn't be decoded
            #TODO: Provide good error message.
            return None

        #Check the status of the response, Login is successful ONLY if stat == 'ok'. 
        if response['stat'] != 'ok':
            #TODO: Check for why we have failure. See https://rpxnow.com/docs
            #      for the error codes.
            return None

        #At this point, we assume that the RPX authentication has been
        #successful. If the user has already been registered, then we return
        #the User object. If the user is not registered, then we return an
        #RpxData object instead. We leave it up to the view to handle 
        #registration.
        
        #All of user's information is contained in 'profile', which is a
        #dictionary of fields forming the user's profile. The keys of the
        #profile fields can be found here: https://rpxnow.com/docs#profile_data
        rpx_profile = response['profile']
        #There are two fields that are guaranteed to be returned for every login
        #so we pull them out for clarity. rpx_identifier is unique for every user
        #so we use as our database key for lookups.
        rpx_identifier = rpx_profile['identifier'] #An OpenID URL
        rpx_provider = rpx_profile['providerName']
        
        #See if this RPX identifier already exists in our RpxData database. 
        try:
            rd = RpxData.objects.get(identifier = rpx_identifier)
            #If user doesn't exist, rd.user will be None.
            if rd.user == None:
                #This means that the user has logged in before but never 
                #registered (ie. created a User object). We refresh the 
                #RpxData object with returned profile information. Then
                #return the RpxData object so that view can handle 
                #registration.
                rd.profile = rpx_profile
                rd.save()
                return rd
        except RpxData.DoesNotExist:
            #If the returned RPX data does not exist in DB, that means this is
            #the first time the user signed into this site. Thus, the user has
            #not registered either. Let's save the login data:
            rd = RpxData()
            rd.identifier = rpx_identifier
            rd.provider = rpx_provider
            rd.profile = rpx_profile
            rd.save()
            
            #We return the RpxData object so that the view can handle
            #registering the user.
            return rd
        
        #Getting here means that user has successfully logged in AND has 
        #previously registered (since we found a User object corresponding
        #to the RpxData object). So we refresh the user's profile with
        #data from RPX, then return the User object.
        rd.profile = rpx_profile
        rd.save()

        return rd.user
