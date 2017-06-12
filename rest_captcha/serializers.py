from rest_framework import serializers
from django.utils.translation import ugettext as _
from django.core.cache import caches
from .settings import api_settings

cache = caches[api_settings.CAPTCHA_CACHE]


class RestCaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField(max_length=64)
    captcha_value = serializers.CharField(max_length=8, trim_whitespace=True)

    def validate(self, data):
        super(RestCaptchaSerializer, self).validate(data)

        real_value = cache.get(data['captcha_key'])

        if real_value is None:
             raise serializers.ValidationError(
                 _('Invalid or expared captcha key'))

        cache.delete(data['captcha_key'])
        if data['captcha_value'] != real_value:
            raise serializers.ValidationError(_('Invalid captcha value'))

        del data['captcha_key']
        del data['captcha_value']
        return data
