# payments/views.py

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def index(request):
    if request.method == 'POST':
        amount = int(request.POST['amount']) * 100  # Convert to paise
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency='INR', payment_capture='1'))
        order_id = razorpay_order['id']
        
        context = {
            'amount': amount,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order_id,
            'callback_url': request.build_absolute_uri('/payments/callback/'),
        }
        return render(request, 'payments/index.html', context)
    return render(request, 'payments/index.html')

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            
            if result:
                return JsonResponse({'status': 'Payment successful'})
            else:
                return JsonResponse({'status': 'Payment failed'})
        except Exception as e:
            return HttpResponseBadRequest()
    return HttpResponseBadRequest()
