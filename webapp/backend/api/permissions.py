from rest_framework import permissions

class BlocklistPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        allow_ip = '127.0.0.1'
        if ip_addr == allow_ip:
            return allow_ip
        
        return request.method in permissions.SAFE_METHODS
        # return bool(
        #     request.method in permissions.SAFE_METHODS or
        #     request.user and
        #     request.user.is_authenticated
        # )