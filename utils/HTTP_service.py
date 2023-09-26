from django.http import HttpRequest


# def get_client_ip(request: HttpRequest):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#
#     if x_forwarded_for:
#         ip = x_forwarded_for.split('.')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip_list = x_forwarded_for.split(',')
        ip = ip_list[-1].strip()  # Take the last IP address
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip