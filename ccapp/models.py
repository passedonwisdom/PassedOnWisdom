# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator , MinValueValidator

year_choices = ( 
    ("FY","FY"), 
    ("SY","SY"), 
    ("TY","TY"), 
    ("LY","LY"), 
) 

branch_choices = ( 
    ("IT","IT"), 
    ("COMPS","COMPS"), 
    ("EXTC","EXTC"), 
    ("ETRX","ETRX"), 
    ("MECH","MECH"), 
) 

#TODO make migration with editable = False
class Student(models.Model):
    email = models.EmailField()
    fullName = models.CharField(max_length=255)
    password = models.CharField(max_length=20,editable = False)
    confirmPassword = models.CharField(max_length=20,editable = False)
    contactNumber= models.CharField(max_length=12, )
    year=models.CharField(max_length = 2, choices = year_choices, default = 'FY') 
    branch=models.CharField(max_length = 5, choices =branch_choices, default = 'IT') 
    def __str__(self):
        return self.email

#products

book_status=( 
    ("pending","pending"),
    ("verified","verified"),
    ("inProcess","inProcess"),
    ("sold","sold"),
) 
class Book(models.Model):
    seller=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="books")
    bookId = models.AutoField(primary_key=True)
    bookImage=models.ImageField(upload_to="images/book",null=True,blank=True,default="images/book/defaultBook.jpg")
    bookName=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    description=models.TextField(blank=True)
    status=models.CharField(max_length = 10, choices = book_status, default = 'pending') 
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.bookName+"_"+self.seller.email

coat_status=(
    ("inStock","inStock"),
    ("inProcess","inProcess"),
    ("sold","sold"),
)

condition=(
    ("used","used"),
    ("new","new"),
)

size_choices=(
    ("S","S"),
    ("M","M"),
    ("L","L"),
    ("XL","XL"),
    ("XXL","XXL"),
)

class Coat(models.Model):
    seller=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="coats")
    coatId = models.AutoField(primary_key=True)
    description=models.TextField(blank=True)
    status=models.CharField(max_length = 10, choices = coat_status, default = 'inStock') 
    size=models.CharField(max_length = 10, choices = size_choices, default = 'L')
    condition=models.CharField(max_length = 4, choices =condition, default = 'used') 
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.seller.email+"_"+self.size

class Suit(models.Model):
    seller=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="suits")
    suitId = models.AutoField(primary_key=True)
    description=models.TextField(blank=True)
    status=models.CharField(max_length = 10, choices = coat_status, default = 'inStock') 
    size=models.CharField(max_length = 10, choices = size_choices, default = 'L') 
    gender=models.CharField(max_length = 10, choices =(("Male","Male"),("Female","Female")), default = 'Male') 
    condition=models.CharField(max_length = 4, choices =condition, default = 'used') 
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.seller.email+"_"+self.size

class Calculator(models.Model):
    seller=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="calculators")
    calculatorId = models.AutoField(primary_key=True)
    condition=models.CharField(max_length = 4, choices =condition, default = 'used')
    description=models.TextField(blank=True)
    status=models.CharField(max_length = 10, choices = coat_status, default = 'inStock')
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.seller.email


#Order

class Order_Book(models.Model):
    book=models.OneToOneField(Book,on_delete=models.CASCADE,related_name="order_books")
    customer=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="order_books")
    timestamp=models.DateTimeField(auto_now_add=True)
    flag_seller_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    flag_customer_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    def __str__(self):
        return self.customer.email+"_"+self.book.bookName+"_"+self.book.seller.email

class Order_Coat(models.Model):
    coat=models.OneToOneField(Coat,on_delete=models.CASCADE,related_name="order_coats")
    customer=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="order_coats")
    timestamp=models.DateTimeField(auto_now_add=True)
    flag_seller_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    flag_customer_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    def __str__(self):
        return self.customer.email+"_"+self.coat.seller.email

class Order_Suit(models.Model):
    suit=models.OneToOneField(Suit,on_delete=models.CASCADE,related_name="order_suits")
    customer=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="order_suits")
    timestamp=models.DateTimeField(auto_now_add=True)
    flag_seller_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    flag_customer_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    def __str__(self):
        return self.customer.email+"_"+self.suit.seller.email

class Order_Calculator(models.Model):
    calculator=models.OneToOneField(Calculator,on_delete=models.CASCADE,related_name="order_calculators")
    customer=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="order_calculators")
    timestamp=models.DateTimeField(auto_now_add=True)
    flag_seller_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    flag_customer_complete=models.CharField(max_length = 1, choices =(("0","0"),("1","1")), default = '0') 
    def __str__(self):
        return self.customer.email+"_"+self.calculator.seller.email


class Order_Toolkit(models.Model):
    customer=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="order_toolkits")
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.customer.email

#feedbacks

class Report_Book(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="report_books")
    customer=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="report_books")
    

class Feedback(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    feedback=models.TextField()
    year=models.CharField(max_length = 2, choices = year_choices, default = 'FY') 
    branch=models.CharField(max_length = 5, choices =branch_choices, default = 'IT')
    def __str__(self):
        return self.email

class DeletedEmails(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email