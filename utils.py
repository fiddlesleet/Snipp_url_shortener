from django.conf import settings
import random
import string

# from shortener.models import SnippURL--throws error

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)


# chars=string.ascii_lowercase == chars="abcdefghijklmnopqrstuvwxyz"; string.digists = "0123456789"
def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
    # new_code = ''
    # # the _ is a shortcut in python for when the var not actually being used, but want 2 run iteration
    # for _ in range(size):
    #     new_code += random.chice(chars)
    # return new_code
    # shorthand for what's above
    return ''.join(random.choice(chars) for _ in range(size))


def create_shortcode(instance, size=SHORTCODE_MIN):  # call in python shell with SnippURL.objects.refresh_shortcodes()
    new_code = code_generator(size=size)
    snippURLClass = instance.__class__  # getClass() in python--like importing class without importing class
    # check code doesn't already exist for this url (could use same function to ensure slugs unique)
    qs_exists = snippURLClass.objects.filter(shortcode=new_code).exists()  # filter is built-in method of Models
    if qs_exists:
        return create_shortcode(size=size)
    return new_code

