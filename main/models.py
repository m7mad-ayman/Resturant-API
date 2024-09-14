from django.db import models
import uuid
# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=100,null=False,blank=False)
    def __str__(self):
        return self.name
    
class Table(models.Model):
    number = models.IntegerField(null=False,unique=True)
    capacity = models.IntegerField(null=False)
    is_available = models.BooleanField(null=False)
    def __str__(self):
        return str(self.number)



class Ingredient(models.Model):
    name= models.CharField(max_length=100,null=False,blank=False)
    quantity = models.DecimalField(max_digits=6,decimal_places=2,null=False)
    unit = models.CharField(max_length=100,null=False)
    threshold = models.DecimalField(max_digits=6,decimal_places=2,null=False) #alert
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200,null=True,unique=True)
    description = models.TextField(null=False)
    price =models.DecimalField(max_digits=6,decimal_places=2,null=True)
    is_available = models.BooleanField(null=False,default=True)
    ingredients = models.ManyToManyField(Ingredient,related_name='rel_ingredient')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='rel_category',null=True)
    def __str__(self):
        return self.name

class IngerdientItem(models.Model):
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    def __str__(self):
        return "{} , {}".format(self.menuitem.name,self.ingredient.name)

class Reservation(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    customer_name = models.CharField(max_length=200,null=False)
    reservation_date = models.DateField(null=False)
    guests_num = models.IntegerField(null=False,blank=False)
    table = models.ForeignKey(Table,null=False,on_delete=models.CASCADE,related_name='rel_table')
    status = models.CharField(max_length=100,null=False,choices=[('pending','pending'),('confirmed','confirmed')],default="pending")
    def __str__(self):
        return self.customer_name



class Order(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    customer_name = models.CharField(max_length=200,null=False)
    order_type = models.CharField(max_length=100,null=False,choices=[('dine-in','dine-in'),('takeaway','takeaway'),('delivery','delivery')])
    delivery = models.DecimalField(max_digits=6,decimal_places=2,null=True,default=30)
    table = models.ForeignKey(Table,null=True,on_delete=models.CASCADE,related_name='order_table')
    order_items = models.ManyToManyField(MenuItem,related_name='rel_items')
    total_price  = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    status = models.CharField(max_length=100,null=False,choices=[('preparing','preparing'),('served','served'),('completed','completed')],default="preparing")
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.customer_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='rel_order')
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name='rel_item')
    quantity = models.IntegerField(null=False,default=1)
    def __str__(self):
        return str(self.order.id)