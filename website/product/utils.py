
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets



class CacheMixins(viewsets.ModelViewSet):
    pass
#    @method_decorator(vary_on_cookie)
#    @method_decorator(cache_page(60 * 1))
#   def dispatch(self, *args, **kwargs):
#        return super(CacheMixins, self).dispatch(*args, **kwargs)


