from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.linkedin_scraper import *

# Create your views here.

class LinkedinLoginView(APIView):
    
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        try:
            # Use existing session if not expired
            session_active = load_cookie_session(username, password)

            if not session_active:
                # If session expired or doesn't exist, login again
                linkedin_login(username, password)
                load_cookie_session()

            return Response({'message': 'Login Successful'}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)




