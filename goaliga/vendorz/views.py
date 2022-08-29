
from django.shortcuts import render

from .serializers import VendorSerilaizer,PackageSerilaizerz,CategorySerilaizer,ItinerarySerilaizer
from .models import Registrationz,VendorToken
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import exceptions
import jwt ,datetime
from trips.models import Packages,Itinerary,Category
from rest_framework import viewsets
from .authentication import *
from django.contrib.auth.hashers import check_password

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail


from vendorz import serializers



# Create your views here.
@api_view(['POST'])
def RegisterVendor(request):
    data = request.data


    if data['password'] != data['confirm_password']:
            raise exceptions.AuthenticationFailed ('password incorrect')
    print(data)        

    vendor = Registrationz.objects.create(
        company_name= data['company_name'],
        company_logo=data['company_logo'],
        adhar_no=data['adhar_no'],
        aadhar_image=data['aadhar_image'],
        office_address=data['office_address'],
        mobile=data['mobile'],
        email=data['email'],
        registration_doc=data['registration_doc'],
        licence_no=data['licence_no'],
        licence_image=data['licence_image'],
        year_of_experience=data['year_of_experience'],
        password=make_password(data['password']))

    print(vendor,"iam vendor")

    send_mail('heloooo ',
            'Thank You For Registering with us,Your Application is underprocess ',
            'aligadrm@gmail.com'
            ,[vendor.email]   
            ,fail_silently=False)
 

    serializer = VendorSerilaizer(vendor,many = False)
    return Response(serializer.data)


class LoginView(APIView):
    def post(self,request):
        
        email = request.data['email']
        password = request.data['password']
        print(email,'emaillll')
        print(password,'passwordddd')
        vendor = Registrationz.objects.filter(email=email).first()
        print(vendor.email,'get emaillllll')
        if vendor is None:
            raise exceptions.AuthenticationFailed ('No Vendor available')

        if  check_password(password, vendor.password):
            
            access_token = create_access_token(vendor.id)
            refresh_token = create_refresh_token(vendor.id)
            print("hellooo")

            VendorToken.objects.create(
                vendor_id = vendor.id,
                token= refresh_token,
                expired_at =  datetime.datetime.utcnow()+datetime.timedelta(days=7),
            )

            response = Response()
            response.set_cookie(key='refresh_token',
                                value=refresh_token, httponly=True)
            response.data = {
                'token': access_token
            }

            return  response   
        else:
             raise exceptions.AuthenticationFailed ('validation error')





  



# class ViewRegs(APIView):
#     authentication_classes = [JWTAuthentication]
#     def get(self,request):
#          token = request.COOKIES.get('jwt')

#          if not token:
#             raise exceptions.AuthenticationFailed ('Authentication Failed')
#          try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])

#          except jwt.ExpiredSignatureError:
#                raise exceptions.AuthenticationFailed ('Unauthenticated')

#          vendor = Registrationz.objects.filter(id = payload['id']).first()
#          serializer = VendorSerilaizer(vendor)
#          return Response(serializer.data) 


class ViewRegs(generics.ListAPIView):
    authentication_classes = [StaffAuthentication]
    queryset = Registrationz.objects.all()
    serializer_class = VendorSerilaizer
    
class LogoutView(APIView):
    def post(self,request):
        response =Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }    
        return response

class ViewdetailRegs(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [StaffAuthentication]
    queryset = Registrationz.objects.all()
    serializer_class = VendorSerilaizer


    
class PackageViewset(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    queryset = Packages.objects.all()
    serializer_class = PackageSerilaizerz
   

class CategoryViewset(viewsets.ModelViewSet):
    authentication_classes = [StaffAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerilaizer


class ItineraryViewset(viewsets.ModelViewSet):
    authentication_classes = [StaffAuthentication]
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerilaizer