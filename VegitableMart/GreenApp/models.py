from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.shortcuts import redirect,reverse

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True)
    profile=models.ImageField(default='profile/user-profile.png',upload_to='profile',null=True,blank=True)

    def __str__(self):
        return str(self.name or self.user)

    @property
    def profileURL(self):
        try:
            url = self.profile.url
        except:
            url = ""
        return url

CATEGORY_CHOICES = (('V', 'Vegitable'),
                    ('F', 'Fruit'),
                    )

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2,null=True)
    offer = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    image=models.ImageField(upload_to='images',null=True,blank=True)
    ship = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url
    @property
    def Product_quantity(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total



class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    ordered_date=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    trans_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_cart(self):
        orderitem = self.orderitem_set.all()
        total = sum([items.total_price for items in orderitem])
        return total

    @property
    def total_quantity(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.ship == False:
                shipping = True
        return shipping






class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    added_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)





    @property
    def total_price(self):
        if self.product.offer:
            total = self.product.offer * self.quantity
        else:
            total=self.product.price*self.quantity
        return total

    def get_absolute_url(self):
        return reverse("detail", kwargs={
            'pk': self.pk
        })




class AddressShip(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

