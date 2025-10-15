from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import stripe
from django.conf import settings
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # à configurer dans settings

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Payload invalide
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Signature invalide
        return HttpResponse(status=400)

    # Gérer l'événement
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Supposons que tu as stocké order_id dans metadata lors de la création de session Stripe
        order_id = session.get('metadata', {}).get('order_id')

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.mark_as_paid()
            except Order.DoesNotExist:
                pass  

    return HttpResponse(status=200)
