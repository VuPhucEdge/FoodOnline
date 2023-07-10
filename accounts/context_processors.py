from vendor.models import Vendor


# vendor processors
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None

    return dict(vendor=vendor)
