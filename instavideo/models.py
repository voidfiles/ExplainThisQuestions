from django.db import models

# Create your models here.


class Video(models.Model):
    """A canonical description of one video"""
    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True, verify_exists=True)
    views = models.IntegerField(blank=False, null=False,default=0)
    video_file = models.FileField(upload_to=video_file)

    class Meta:
        ordering = ('',)
        get_latest_by = ''
        verbose_name_plural = ('Videos',)

    def __unicode__(self):
        return u"Video"
    
    def get_absolute_url(self):
        return "/Video/%s" % (self.id,)

