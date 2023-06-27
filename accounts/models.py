from django.db import models
from django.contrib.auth.models import User, AbstractUser
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Product


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    is_email_verify = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile")
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, default='N/A')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False, cart__user=self.user).count()


class Cart(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="carts")
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
        print(price)
        return sum(price)


class CartItems(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        price = [self.product.price]

        return sum(price)


class Order(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(
        Product, related_name="orders", blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('PENDING', 'Pending'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled'),
        ),
        default='PENDING'
    )
    order_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)
