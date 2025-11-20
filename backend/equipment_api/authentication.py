from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session authentication that doesn't enforce CSRF checks.
    Use only for development!
    """
    def enforce_csrf(self, request):
        return  # Do not enforce CSRF check
