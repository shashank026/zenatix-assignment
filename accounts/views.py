import json
from multiprocessing import context
from os import access
from unicodedata import category
from middleware.session import JWTAccessTokenMiddleware
from cProfile import Profile
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from products.models import *
from accounts.models import Cart, CartItems
from accounts.models import Profile, Order
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.decorators import method_decorator
import jwt
import datetime

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            return JsonResponse({'status': 400, 'message': "Account not found."})

        if user_obj[0].profile.is_blocked:
            return JsonResponse({'status': 403, 'message': "Your account is blocked."})

        if not user_obj[0].profile.is_email_verify:
            return JsonResponse({'status': 400, 'message': "Your account is not verified."})

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            current_time = datetime.datetime.utcnow()
            # Set expiration time to 30 minutes from now
            expiration_time = current_time + datetime.timedelta(minutes=60)

            # Include the 'exp' claim in the payload
            payload = {'email': email, 'exp': expiration_time}
            jwt_token = jwt.encode(payload, 'secret_key', algorithm='HS256')

            response = JsonResponse({'status': 200, 'message': "Login Successfully.",
                                     'access_token': jwt_token})
            # Set the cookie with the JWT token
            response.set_cookie('jwt_access_token', jwt_token, httponly=True)
            return response

        return JsonResponse({'status': 403, 'message': "Invalid Credentials."})

    elif request.method == 'GET':
        access_token = request.COOKIES.get('jwt_access_token')

        if access_token:
            try:
                decoded_token = jwt.decode(
                    access_token, 'secret_key', algorithms=['HS256'])
                return redirect('/accounts/profile/')

            except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
                response = redirect('/')
                response.delete_cookie('jwt_access_token')
                return response

            except Exception as e:
                print(e)
                return JsonResponse({'status': 500, 'message': "Internal Server Error."})

        return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


def adminlogin(request):
    try:
        if request.user:
            if request.method == 'POST':
                email = request.POST.get('username')
                password = request.POST.get('password')
                user_obj = User.objects.filter(username=email)
                print(user_obj)
                if not user_obj[0].profile.is_admin:
                    return JsonResponse({'status': 403, 'message': 'Access denied.'})

                user = authenticate(username=email, password=password)

                if user is not None:
                    login(request, user)
                    current_time = datetime.datetime.utcnow()
                    # Set expiration time to 30 minutes from now
                    expiration_time = current_time + \
                        datetime.timedelta(minutes=60)

                    # Include the 'exp' claim in the payload
                    payload = {'email': email, 'exp': expiration_time}
                    jwt_token = jwt.encode(
                        payload, 'secret_key', algorithm='HS256')

                    response = JsonResponse({'status': 200, 'message': "Login Successfully.",
                                            'access_token': jwt_token})
                    # Set the cookie with the JWT token
                    response.set_cookie('jwt_access_token',
                                        jwt_token, httponly=True)
                    return response

                return JsonResponse({'status': 403, 'message': "Invalid Credentials."})
            return render(request, 'accounts/adminlogin.html')
        return render(request, 'accounts/adminlogin.html')
    except Exception as e:
        print(e)


def admindashboard(request):
    print(request.user)
    if not request.user.is_anonymous:
        try:
            adminUser = User.objects.filter(username=request.user)
            if not adminUser[0].profile.is_admin:
                return redirect('/accounts/login/')
            users = User.objects.all()  # Retrieve all users from the database
            profile = Profile.objects.all()
            order = Order.objects.all()
            product = Product.objects.all()
            return render(request, 'accounts/admindashboard.html', {'users': users, 'profiles': profile, "orders": order, 'products': product, 'categorys': category})
        except Exception as e:
            print("EXCEPTION: ", e)
    return redirect('/accounts/login/')


def register_page(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=email)

            if user_obj.exists():
                return JsonResponse({'status': 403, 'message': "Email is already taken."})

            user_obj = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email
            )
            user_obj.set_password(password)
            user_obj.save()

            # Create or update the Profile object for the user and set the phone number
            profile, created = Profile.objects.get_or_create(user=user_obj)
            profile.phone_number = phone_number
            profile.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user_obj)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return JsonResponse({'status': 200, 'message': "An email has been sent on your mail.",
                                'access_token': access_token, 'refresh_token': refresh_token})

        except Exception as e:
            return JsonResponse({'status': 400, 'message': "Something went wrong please try again.",
                                'access_token': access_token, 'refresh_token': refresh_token})
    return render(request, 'accounts/register.html')


def logout(request):
    if request.method == 'POST':
        # Perform logout actions
        auth_logout(request)
        print("request recieve")

        # Clear the JWT access token cookie
        response = JsonResponse(
            {'status': 200, 'message': 'Logout successfully'})
        response.delete_cookie('jwt_access_token')
        return response
    else:
        return JsonResponse({'status': 400, 'message': 'Something went wrong. Please try again.'})


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verify = True
        user.email_token = None
        user.save()
        return redirect('/')
    except Profile.DoesNotExist:
        return JsonResponse({'status': 400, 'message': "Token has been expired."})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 400, 'message': "Invalid Token"})


def remove_cart_item(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
        return JsonResponse({'status': 400, 'message': 'Error removing item from cart.'})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_to_cart(request, uid):
    try:
        # access_token = request.COOKIES.get('jwt_access_token')
        # print(access_token)
        product = Product.objects.get(uid=uid)
        # user = Profile.objects.get(email=email)
        user = request.user
        # print(user)
        if user.is_anonymous:
            return redirect('/accounts/login/')
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
        cart_item = CartItems.objects.create(cart=cart, product=product)
        cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print("Error from this: ", e)


def cart(request):
    try:
        if request.user.id == None:
            print('Check Success')
            return redirect('/accounts/login/')
        else:
            context = {'cart': Cart.objects.filter(
                is_paid=False, user=request.user).first()}
            return render(request, 'accounts/cart.html', context)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 400, 'message': 'Something went wrong please try again.'})


def profile(request):
    try:
        if request.user.id == None:
            return redirect('/accounts/login')

        user = request.user
        order_history = Order.objects.filter(user=user)
        context = {
            'order_history': order_history
        }
        return render(request, 'accounts/profile.html', context)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 400, 'message': 'User not found, please login.'})


def placedOrder(request):
    if request.method == 'POST':
        try:
            user = request.user
            cart = Cart.objects.get(user=user, is_paid=False)
            cart_items = cart.cart_items.all()
            print(cart_items)

            # Calculate the total amount based on cart items
            total_amount = json.loads(request.body).get('total_amount')
            print(total_amount)
            if total_amount == 0:
                return JsonResponse({'status': 400, 'message': 'Please add items in cart to place order.'})

            # Create the order
            order = Order.objects.create(
                user=user,
                total_amount=total_amount,
                status='PENDING'
            )
            print(order)
            # Move cart items to the order
            # Move cart items to the order and add multiple products to the order
            for item in cart_items:
                order.products.add(item.product)

            # Mark the cart as paid
            cart.is_paid = True
            cart.save()

            return JsonResponse({'status': 200, 'message': 'Order placed successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 400, 'message': 'Error occured while confirming the order.'})


def AdminChangeOrderStatusView(request):
    if request.method == 'POST':
        try:
            print(request.user)
            adminUser = User.objects.filter(username=request.user).first()
            print(adminUser)
            if request.user.is_anonymous or not adminUser.profile.is_admin:
                return JsonResponse({'status': 403, 'message': 'Forbiden Access denied'})
            print('Entered Here')
            order_id = json.loads(request.body).get('order_id')
            order = Order.objects.get(order_id=order_id)
            print('Ordered')
            status = json.loads(request.body).get('status')
            print('Status')
            print(order)
            print(status)

            # Perform any validation or checks on the status value

            order.status = status
            order.save()

            return JsonResponse({'status': 200, 'message': 'Order status changed successfully.'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 400, 'message': 'Order not found.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 500, 'message': 'Internal Server Error.'})
    else:
        return JsonResponse({'status': 403, 'message': 'Forbiden Access denied'})


def AdminBlockUnblockUser(request):
    if request.method == 'POST':
        try:
            print(request.user)
            adminUser = User.objects.filter(username=request.user).first()
            print(adminUser)
            if request.user.is_anonymous or not adminUser.profile.is_admin:
                return JsonResponse({'status': 403, 'message': 'Forbiden Access denied'})
            email = json.loads(request.body).get('email')
            user_obj = User.objects.get(username=email)
            profile = Profile.objects.get(user=user_obj)
            if profile.is_admin:
                return JsonResponse({'status': 403, 'message': 'User is Admin, You are not allowed to block admin.'})

            # Perform any validation or checks on the status value
            if profile.is_blocked:
                profile.is_blocked = False
                profile.save()
                return JsonResponse({'status': 200, 'message': 'User Unblocked successfully.'})
            else:
                profile.is_blocked = True
                profile.save()
                return JsonResponse({'status': 200, 'message': 'User Blocked successfully.'})

        except Profile.DoesNotExist:
            return JsonResponse({'status': 400, 'message': 'User not found.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 500, 'message': 'Internal Server Error.'})
    else:
        return JsonResponse({'status': 403, 'message': 'Forbiden Access denied'})


def AdminAddProduct(request):
    if request.method == 'POST':
        try:
            print(request.user)
            adminUser = User.objects.filter(username=request.user).first()
            print(adminUser)
            if request.user.is_anonymous or not adminUser.profile.is_admin:
                return JsonResponse({'status': 403, 'message': 'Forbiden Access denied'})
            product_name = request.POST.get('product_name')
            price = request.POST.get('price')
            product_description = request.POST.get('product_description')
            product_quantity = request.POST.get('product_quantity')
            # Get the uploaded image file
            image_file = request.FILES.get('image')

            # Perform any additional validation or data processing here
            category, _ = Category.objects.get_or_create(
                category_name="digital camers")
            # Create the new product
            # Create the new product
            product = Product(
                product_name=product_name,
                price=price,
                product_description=product_description,
                product_quantity=product_quantity,
                category=category,
            )
            product.save()

            # Create the product image
            product_image = ProductImage(product=product, image=image_file)
            product_image.save()

            return JsonResponse({'message': 'Product added successfully.'})

        except Exception as e:
            print(e)
            return JsonResponse({'status': 500, 'message': 'Internal Server Error.'})
    else:
        return JsonResponse({'status': 403, 'message': 'Forbiden Access denied'})


def AdminUpdateProductDetails(request):
    if request.method == 'POST':
        try:
            adminUser = User.objects.filter(username=request.user).first()
            if request.user.is_anonymous or not adminUser.profile.is_admin:
                return JsonResponse({'status': 403, 'message': 'Forbidden Access denied'})

            product_name = request.POST.get('product_name')
            price = request.POST.get('price')
            product_quantity = request.POST.get('product_quantity')
            image_file = request.FILES.get('image')
            print(image_file)
            final_price = (int(''.join(filter(str.isdigit, price))) // 100)

            # Retrieve the product to be updated
            product_id = request.POST.get('product_uid')
            product = Product.objects.get(uid=product_id)

            # Update the product details
            product.product_name = product_name
            product.price = final_price
            product.product_quantity = product_quantity

            if image_file:
                # Save the new product image
                product_image = ProductImage.objects.get(product=product)
                print(product_image)
                product_image.image = image_file
                print(product_image.image)
                product_image.save()

            product.save()

            return JsonResponse({'status': 200, 'message': 'Product details updated successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 500, 'message': 'Internal Server Error.'})
    else:
        return JsonResponse({'status': 403, 'message': 'Forbidden Access denied'})
