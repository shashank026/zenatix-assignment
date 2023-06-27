from django.shortcuts import render
import jwt


class JWTAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('jwt_access_token')
        if not request.path == '/accounts/logout/' and access_token:
            try:
                # Decode the access token and check if it's expired
                decoded_token = jwt.decode(access_token, 'secret_key', algorithms=['HS256'])
            except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
                # Handle the exception as per your requirement
                return render(request, 'base/session.html')

        response = self.get_response(request)
        return response
