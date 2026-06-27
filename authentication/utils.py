def get_client_ip(request):
    """
    Utility to get the client IP address from a Django request object.
    Checks the HTTP_X_FORWARDED_FOR header first, then REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
