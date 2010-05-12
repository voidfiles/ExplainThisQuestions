from django.db import models
from picklefield.fields import PickledObjectField

class RpxData(models.Model):
    #Primary key field is automatically created.
    
    #The RPX identifier is essentially an OpenID URL.
    identifier = models.URLField(unique = True, verify_exists = False,
                                 max_length = 255, db_index = True)
    #The name of the auth provider (eg. Google, Twitter, Facebook, etc.).
    provider = models.CharField(max_length = 255)
    
    #The User field can be null if the user has logged in but did not 
    #register an account (thus creating an associated User object).
    user = models.ForeignKey('auth.User', null = True)
    
    #We pickle and store the profile dict because: 1) We only have a 10 min
    #window where we can grab user info data from RPX after auth. So there may
    #be times when we want to access extra user data but don't feel like making
    #the user login again. 2) The profile can contain any number of fields and 
    #not all of them are guaranteed. So it's messy to create a table for each of
    #the fields, especially since we will rarely access this data anyway.
    profile = PickledObjectField()

    def __unicode__(self):
        return u"RPX identifier is %s" % self.identifier
        
