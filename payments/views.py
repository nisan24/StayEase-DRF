from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment_Model, Booking_Model
from sslcommerz_lib import SSLCOMMERZ
import uuid, time
from payments.models import Payment_Model
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from django.http import HttpResponseRedirect


class Payment_View(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        booking_id = request.data.get('booking_id')
        
        try:
            booking = Booking_Model.objects.get(id= booking_id)
        except Booking_Model.DoesNotExist:
            return Response({'message': 'Booking not found'}, status= status.HTTP_404_NOT_FOUND)

        if booking.payment_status == 'Paid':
            return Response({'message': 'This booking has already been paid for.'}, status= status.HTTP_400_BAD_REQUEST)


        settings_data = {
            'store_id': settings.STORE_ID,
            'store_pass': settings.STORE_PASS,
            'issandbox': settings.IS_SANDBOX
        }
        
        sslcz = SSLCOMMERZ(settings_data)

        # Unique transaction ID bananor jonno 
        # transaction_id = str(uuid.uuid4())
        transaction_id = f"TXN-B{booking_id}U{request.user.id}-{str(uuid.uuid4())[:8].upper()}"

        # transaction_id = f"{str(uuid.uuid4())[:8]}-{int(time.time())}"

        post_body = {
            'total_amount': booking.total_price,
            'currency': "BDT",
            'tran_id': transaction_id,
            'success_url': "http://127.0.0.1:8000/api/payment/success/",
            'fail_url': "http://127.0.0.1:8000/api/payment/fail/",
            'cancel_url': "http://127.0.0.1:8000/api/payment/cancel/",
            'emi_option': 0,
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_phone': "01700000000",
            'cus_add1': "Test Address",
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'product_name': booking.hotel.name,
            'num_of_item': 1,
            'product_category': "Hotel Booking",
            'product_profile': "general",
        }

        response = sslcz.createSession(post_body)
        print(response)
           
        if response.get('status') == 'SUCCESS':
            try:
                Payment_Model.objects.create(
                    user= request.user,
                    booking= booking,
                    amount= booking.total_price,
                    payment_status= 'Pending',
                    transaction_id= transaction_id
                )
                return Response(
                    {
                        "status": "success",
                        "tran_id": transaction_id,
                        "message": f"Payment session created successfully for booking: {booking.hotel.name}",
                        "payment_url": response.get('GatewayPageURL'),
                    },
                    status= status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {
                        "status": "error",
                        "message": "Failed to create payment.",
                        "details": str(e)
                    },
                    status= status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {
                    "status": "error",
                    "message": "Payment session creation failed.",
                    "details": response
                },
                status= status.HTTP_400_BAD_REQUEST
            )


# =================================


class PaymentSuccess_View(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        tran_id = request.data.get('tran_id')
        if not tran_id:
            return Response({'message': 'Transaction ID is required.'}, status= status.HTTP_400_BAD_REQUEST)
        
        try:
            payment = Payment_Model.objects.get(transaction_id= tran_id)
            
            if payment.payment_status == 'Completed':
                return Response({'message': 'Payment already completed.'}, status= status.HTTP_400_BAD_REQUEST)

            payment.payment_status = 'Completed'
            payment.save()

            booking = payment.booking
            if booking.payment_status == 'Paid':
                return Response({'message': 'This booking is already paid and confirmed.'}, status= status.HTTP_400_BAD_REQUEST)

            booking.payment_status = 'Paid'
            booking.is_confirmed = True
            booking.payment_reference = tran_id
            booking.save()
            
            
            return HttpResponseRedirect("http://127.0.0.1:5500/booking-history.html")

            # return Response(
            #     {
            #         'message': 'Payment successful!',
            #         'tran_id': tran_id,
            #         'booking_id': booking.id,
            #         'hotel_name': booking.hotel.name,
            #         'room_type': booking.room.room_type if booking.room else None,
            #         'total_price': booking.total_price
            #     },
            #     status= status.HTTP_200_OK
            # )
        except Payment_Model.DoesNotExist:
            return Response({'message': 'Invalid transaction ID!'}, status= status.HTTP_400_BAD_REQUEST)




class PaymentFail_View(APIView):
    def post(self, request):
        tran_id = request.data.get('tran_id')
        if not tran_id:
            return Response({'message': 'Transaction ID is required.'}, status= status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment_Model.objects.get(transaction_id= tran_id)
            
            payment.payment_status = 'Failed'
            payment.save()

            return HttpResponseRedirect("http://127.0.0.1:5500/index.html")

            # return Response({'message': 'Payment failed!', 'transaction_id': tran_id}, status= status.HTTP_200_OK)

        except Payment_Model.DoesNotExist:
            return Response({'message': 'Invalid transaction ID!'}, status= status.HTTP_400_BAD_REQUEST)




class PaymentCancel_View(APIView):
    def post(self, request):
        tran_id = request.data.get('tran_id')
        if not tran_id:
            return Response({'message': 'Transaction ID is required.'}, status= status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment_Model.objects.get(transaction_id= tran_id)
            
            payment.payment_status = 'Cancelled'
            payment.save()

            return HttpResponseRedirect("http://127.0.0.1:5500/index.html")
            # return Response({'message': 'Payment cancelled!', 'transaction_id': tran_id}, status= status.HTTP_200_OK)

        except Payment_Model.DoesNotExist:
            return Response({'message': 'Invalid transaction ID!'}, status= status.HTTP_400_BAD_REQUEST)


# ====

# payment json:
    
# {
#     "booking_id": 1
# }

# ===

# booking json:
# {
#   "hotel": 2,
#   "room": 1,
#   "start_date": "2025-02-24",
#   "end_date": "2025-02-25",
#   "guests": 2,
#   "contact_number": "01639000000",
#   "email": "nisanhossain24@gmail.com"
# }
