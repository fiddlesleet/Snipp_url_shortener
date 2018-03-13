from django.conf import settings
from django.db import models
from django.utils.encoding import smart_text
from django_hosts.resolvers import reverse
from .utils import code_generator, create_shortcode
from .validators import validate_dot_com, validate_url
# Create your models here.

# gets max from settings.py, but has default if we change the field name in settings.py and forget to update it here
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 30)


class SnippURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(SnippURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)  # filters down qs so only the entries that meet this criterion are left
        return qs

    # change all shortcodes all at once
    def refresh_shortcodes(self, items=None):  # items == number of items we want to refresh
        qs = SnippURL.objects.filter(id__gte=1)  # gte == greater than or equal to; grabs every item

        # reverses order of ids (can also do ('-url')
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        new_shortcodes = 0

        for q in qs:
            # if q.shortcode = "defaultshortcode", see (*) below.; this function seria mas util if u had a defaultval
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            new_shortcodes += 1

        return "New shortcodes generated: {i}".format(i=new_shortcodes)


class SnippURL(models.Model):
    url = models.CharField(max_length=220, validators=[validate_url, validate_dot_com])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)  # Nowhere should the shortcodes be the same
    updated = models.DateTimeField(auto_now=True)                         # updates time value everytime model saved
    timestamp = models.DateTimeField(auto_now_add=True)                   # stamps when model was created
    active = models.BooleanField(default=True)

    objects = SnippURLManager()

    # override default save method
    def save(self, *args, **kwargs):
        # only generate shortcode if one for this url does not already exist in db
        if self.shortcode is None or self.shortcode == "":
            # calls save method in class we're inheriting from--in this case models.Model (see SnippURL def)
            self.shortcode = create_shortcode(self)  # generate unique shortcode
        if not "http" in self.url:
            self.url = "http://" + self.url
        super(SnippURL, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text(self.url)

    def __unicode__(self):
        return smart_text(self.url)

    def get_short_url(self):
        url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='www', scheme="http")
        return url_path


    # Other field options:
    # (*) shortcode    = models.CharField(max_length=30, default="defaultshortcode", blank=True)
    # a date/time field you can edit within admin panel:
    #   blank_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    # shortcode = models.CharField(max_length=30, null=True)    # Empty in db is okay
    # shortcode = models.CharField(max_length=30 default='snippdefaultshortcode')

    # link in overridden ModelManager (the class above) & its functions

    # class Meta:
    #   ordering = ['-id'] (order by reverse id (can also do '-url', etc)

