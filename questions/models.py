from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
# Create your models here.
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.db import IntegrityError

class UserProfile(models.Model):
    """A user profile"""

    
    user = models.ForeignKey(User, unique=True)
    user_type = models.IntegerField(default=1)
    url = models.URLField(blank=True, verify_exists=False)
    bio = models.TextField(blank=True)
    tags = TaggableManager()
    slug = models.SlugField(unique=True,max_length=100)
    
    def save(self, *args, **kwargs): 
        if not self.pk and not self.slug:
            self.slug = slug = slugify(self.user.username)
            i = 0
            while True:
                if self.user.username == "profile":
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
                    
                try:
                    return super(UserProfile, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
        else:
            return super(UserProfile, self).save(*args, **kwargs)
            
    class Meta:
        verbose_name_plural = 'UserProfiles'

    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return "/user/%s" % (self.slug)
        
def createUserProfile(sender, **kwargs):
    created = kwargs.get("created", None)
    instance = kwargs.get("instance", None)
    
    if created and instance:
        userprofile = UserProfile(user=instance)
        userprofile.save()
        
    return True

post_save.connect(createUserProfile,sender=User)


class Site(models.Model):
    """A Site"""
    
    name = models.CharField(blank=True, max_length=255,unique=True)
    url = models.URLField(blank=True, verify_exists=False,unique=True)
    description = models.TextField(blank=True)
    admins = models.ManyToManyField(User)
    
    slug = models.SlugField(unique=True,max_length=100)
    tags = TaggableManager()
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Sites'
        
        
    def save(self, *args, **kwargs): 
        if not self.pk and not self.slug:
            self.slug = slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(Site, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
        else:
            return super(Site, self).save(*args, **kwargs)
            
    def __unicode__(self):
        return u"site: %s" % (self.name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('site_view', (), {
                'widget_type':"site",
                'site_slug': self.slug})
                

        
class Comment(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    added = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        ordering = ('-added',)
    
    


class Question(models.Model):
    """a question"""
    
    title = models.CharField(blank=False, max_length=140)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True,auto_now=True)
    answered = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=True, null=True)
    votes = models.IntegerField(default=0)
    site = models.ForeignKey(Site)
    slug = models.SlugField(unique=True,max_length=100)
    
    comments = generic.GenericRelation(Comment)
    tags = TaggableManager()
    
    
    def sorted_answers(self):
        from voting.models import Vote
        answers = self.answer_set.all()
        scores = Vote.objects.get_scores_in_bulk(answers)
        answers_list = []
        for answer in answers:
            score = 0
            votes = 0
            if answer.id in scores:
                score = scores[answer.id]["score"]
                votes = scores[answer.id]["num_votes"]
            
            answers_list.append([score,votes,answer])
            
        answers_list.sort()
        answers_list.reverse()
        return answers_list
    def save(self, *args, **kwargs): 
        if not self.pk and not self.slug:
            self.slug = slug = slugify(self.title)
            i = 0
            while True:
                try:
                    return super(Question, self).save(*args, **kwargs)
                except IntegrityError, e:
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
        else:
            return super(Question, self).save(*args, **kwargs)
            
    class Meta:
        ordering = ('title',)
        get_latest_by = ''
        verbose_name_plural = 'Questions'


        
    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('question_view', (), {
                'widget_type':"site",
                'site_slug': self.site.slug,
                'question_slug':self.slug})
        
class Answer(models.Model):
    """an answer to a question"""
    
    question = models.ForeignKey(Question)
    description = models.TextField(blank=False,unique=True,verbose_name="Give Us Your Answer")
    created = models.DateTimeField(blank=True,auto_now_add=True)
    updated = models.DateTimeField(blank=True,auto_now_add=True,auto_now=True)
    the_answer = models.BooleanField(default=False)
    user = models.ForeignKey(User,blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    
    comments = generic.GenericRelation(Comment)
    
    class Meta:
        ordering = ('votes','-created')
        verbose_name_plural = 'Answers'

    def __unicode__(self):
        return u"Answer"
    
    def get_absolute_url(self):
        return "%s#answer%s" % (self.question.get_absolute_url(), self.id )
        


    

