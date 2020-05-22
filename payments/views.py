from django.shortcuts import render
from django.http import HttpResponse

import razorpay
client = razorpay.Client(auth=("rzp_test_cOPqeQU2XYK7Xr", "5R2Yk2b5pqQFWfDPFYckvZoz"))

def testing(request):
    return render(request, 'order.html', {})

def create_order(request):
    context = {}
    if request.method == 'POST':
        print("INSIDE Create Order!!!")
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        product = request.POST.get('product')
        order_amount = 0
        if product == 'p1':
            order_amount = 10000
        elif product == 'p2':
            order_amount = 20000
        elif product == 'p3':
            order_amount = 50000
        elif product == 'p4':
            order_amount = 100000

        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'New Delhi'}

        # CREATING ORDER
        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']
        if order_status=='created':
            # Server data for user convinience
            context['product_id'] = product
            context['price'] = order_amount/100
            context['name'] = name
            context['phone'] = phone
            context['email'] = email

            # Data that'll be send to the razorpay for
            context['order_id'] = order_id


            return render(request, 'confirm_order.html', context)
        
    return HttpResponse('<h1>Error in  create order function</h1>')



def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }
    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)
        return render(request, 'order_summary.html', {'status': 'Payment Successful'})
    except:
        return render(request, 'order_summary.html', {'status': 'Payment Faliure!!!'})
