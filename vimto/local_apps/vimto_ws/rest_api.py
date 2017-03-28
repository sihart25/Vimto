''' API for the BWS REST resources. '''
import datetime
import logging
import shutil
import tempfile

from django.conf import settings
from rest_framework import serializers, status
from rest_framework.authentication import BasicAuthentication, \
    TokenAuthentication, SessionAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.exceptions import NotAcceptable
from rest_framework.compat import is_authenticated
# from Vimto.decorator import profile


logger = logging.getLogger(__name__)


class LogThrottleMixin():
    """ Add logging for occasions when throttle stops request. """

    def allow_request(self, request, view):
        """ Implement the check to see if the request should be throttled. """
        success = super(LogThrottleMixin, self).allow_request(request, view)
        if not success:
            return self.throttle_fail(request.user)
        return success

    def throttle_fail(self, user):
        """ Called when a request to the API has failed due to throttling. """
        logger.warning("Request throttled (" + self.__class__.__name__ + "); USER: " + str(user))
        return False


class BurstRateThrottle(LogThrottleMixin, UserRateThrottle):
    """ Throttle short burst of requests from a user. """
    scope = 'burst'


class SustainedRateThrottle(LogThrottleMixin, UserRateThrottle):
    """ Throttle sustained requests from a user. """
    scope = 'sustained'


class EndUserIDRateThrottle(LogThrottleMixin, SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a given end user.
    The end user id plus the user will be used as a unique cache key.
    """
    scope = 'enduser_burst'

    def get_cache_key(self, request, view):
        if is_authenticated(request.user):
            ident = str(request.user.pk)
        else:
            ident = str(self.get_ident(request))

        try:
            ident = ident+"$"+request.data.get('user_id')
            return self.cache_format % {
                'scope': self.scope,
                'ident': ident
            }
        except TypeError:
            return None


class Vimto_wsInputSerializer(serializers.Serializer):
    ''' Vimto result. '''
    user_id = serializers.CharField(min_length=4, max_length=40, required=True)
    pedigree_data = serializers.CharField()




class Vimto_wsOutputSerializer(serializers.Serializer):
    """ Vimto result. """
    version = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    mutation_frequency = serializers.DictField(read_only=True)
    mutation_sensitivity = serializers.DictField(read_only=True)
    cancer_incidence_rates = serializers.CharField(read_only=True)
    warnings = serializers.ListField(read_only=True, required=False)



class Vimto_wsView(APIView):
    renderer_classes = (XMLRenderer, JSONRenderer, BrowsableAPIRenderer, )
    serializer_class = Vimto_wsInputSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    throttle_classes = (BurstRateThrottle, SustainedRateThrottle, EndUserIDRateThrottle)

    def get_serializer_class(self):
        return Vimto_wsInputSerializer

    # @profile("profile_vimto_ws.profile")
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
