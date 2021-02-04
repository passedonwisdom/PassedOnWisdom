from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Student, Book,Suit, Coat, Calculator, Order_Book,Order_Suit, Order_Coat, Order_Calculator, Order_Toolkit, Report_Book, Feedback, DeletedEmails

from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings 
from django.core.mail import send_mail 

# Create your views here.
def index(request):
    return render(request,"index.html")


def login(request):
    err=""
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            if DeletedEmails.objects.filter(email=username).exists():
                err = 'Your account has been deleted.'
                spam=DeletedEmails.objects.all()
                for e in spam:
                    Student.objects.filter(email=e.email).delete()
                    User.objects.filter(email=e.email).delete()
            else:
                auth.login(request, user)
                return redirect('buyAProduct')
        else:
           err = 'Input correct email and password'
    template_name = 'login.html'
    context={'err':err}
    return render(request, template_name,context)

def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    err=""
    if request.method == 'POST':
        email = request.POST.get('email')
        if Student.objects.filter(email = email).exists():
            err = 'Email already taken. Try a different one.'

        else:
            obj1 = User.objects.create(
                username = email,
                email = email,
            )
            obj1.set_password(request.POST.get('password'))
            obj1.save()
            fullName = request.POST.get('fullName')  
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmPassword')
            
            password=make_password(password)
            confirmpassword=password
            print(password)
            contactNumber = request.POST.get('contactNumber')
            year = request.POST.get('year')
            branch = request.POST.get('branch')
            obj2 = Student.objects.create(
                email = email,
                fullName = fullName,
                password = password,
                confirmPassword = confirmpassword,
                contactNumber = contactNumber,
                year = year,
                branch = branch
            )
            obj2.save()
            subject = 'Welcome to passed on wisdom.'
            message = 'Helloo ' +str(fullName) + ' Welcome to passed on wisdom.'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email, ] 
            send_mail( subject, message, email_from, recipient_list )
            return redirect("login")
    template_name = 'login.html'
    context={'err':err}
    return render(request, template_name,context)

@login_required(login_url="login")
def profile(request):
    email = request.user.username
    if request.method=='POST':
        # obj1 = User.objects.get(
        #     email = email,
        # )
        # obj1.set_password(request.POST.get('password'))
        # obj1.save()
        # password = request.POST.get('password')
        # confirmpassword = request.POST.get('confirmPassword')
        contactNumber = request.POST.get('contactNumber')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        Student.objects.filter(email=email).update(
            # password = password,
            # confirmPassword = confirmpassword,
            contactNumber = contactNumber,
            year = year,
            branch = branch
        )
        # user = authenticate(request, username = request.user.email, password = request.POST.get('password'))
        # auth.login(request, user)
    template_name = 'profile.html'
    student=Student.objects.get(email=request.user.username)
    
    # Books
    count_bought_inProcess=Order_Book.objects.filter(customer=student).exclude(flag_seller_complete=1,flag_customer_complete=1).count()
    count_bought_total=Order_Book.objects.filter(customer=student).count()
    count_bought_complete=count_bought_total-count_bought_inProcess

    # count_sold_total=Book.objects.filter(seller=student).count()
    count_sold_pending=Book.objects.filter(seller=student,status="pending").count()
    count_sold_inProcess=Book.objects.filter(seller=student,status="inProcess").count()
    count_sold_sold=Book.objects.filter(seller=student,status="sold").count()
    count_sold_verified=Book.objects.filter(seller=student,status="verified").count()
    
    #suits
    count_bought_inProcess_suit=Order_Suit.objects.filter(customer=student).exclude(flag_seller_complete=1,flag_customer_complete=1).count()
    count_bought_total_suit=Order_Suit.objects.filter(customer=student).count()
    count_bought_complete_suit=count_bought_total_suit-count_bought_inProcess_suit

    # count_sold_total=Book.objects.filter(seller=student).count()
    count_sold_inProcess_suit=Suit.objects.filter(seller=student,status="inProcess").count()
    count_sold_sold_suit=Suit.objects.filter(seller=student,status="sold").count()
    count_sold_inStock_suit=Suit.objects.filter(seller=student,status="inStock").count()

    #Coat
    count_bought_inProcess_coat=Order_Coat.objects.filter(customer=student).exclude(flag_seller_complete=1,flag_customer_complete=1).count()
    count_bought_total_coat=Order_Coat.objects.filter(customer=student).count()
    count_bought_complete_coat=count_bought_total_coat-count_bought_inProcess_coat

    # count_sold_total=Book.objects.filter(seller=student).count()
    count_sold_inProcess_coat=Coat.objects.filter(seller=student,status="inProcess").count()
    count_sold_sold_coat=Coat.objects.filter(seller=student,status="sold").count()
    count_sold_inStock_coat=Coat.objects.filter(seller=student,status="inStock").count()
    
    #Coat
    count_bought_inProcess_calc=Order_Calculator.objects.filter(customer=student).exclude(flag_seller_complete=1,flag_customer_complete=1).count()
    count_bought_total_calc=Order_Calculator.objects.filter(customer=student).count()
    count_bought_complete_calc=count_bought_total_calc-count_bought_inProcess_calc

    # count_sold_total=Book.objects.filter(seller=student).count()
    count_sold_inProcess_calc=Calculator.objects.filter(seller=student,status="inProcess").count()
    count_sold_sold_calc=Calculator.objects.filter(seller=student,status="sold").count()
    count_sold_inStock_calc=Calculator.objects.filter(seller=student,status="inStock").count()

    count_bought_toolkit=Order_Toolkit.objects.filter(customer=student).count()

    total_inProcess_bought=count_bought_inProcess+count_bought_inProcess_calc+count_bought_inProcess_coat+count_bought_inProcess_suit

    total_complete_bought=count_bought_complete+count_bought_complete_calc+count_bought_complete_coat+count_bought_complete_suit+count_bought_toolkit

    total_inProcess_sold=count_sold_inProcess+count_sold_inProcess_calc+count_sold_inProcess_coat+count_sold_inProcess_suit

    total_complete_sold=count_sold_sold+count_sold_sold_calc+count_sold_sold_coat+count_sold_sold_suit

    total_inStock_sold=count_sold_inStock_suit+count_sold_inStock_calc+count_sold_inStock_coat+count_sold_verified+count_sold_pending

    #pending books to verify
    #TODO ask how toolkit is getting processed
    # print(request.user.email)
    # print(Student.objects.get(email=request.user.email).email)
    context={'student':Student.objects.get(email=email),'total_inProcess_bought':total_inProcess_bought,'total_complete_bought':total_complete_bought,'total_inProcess_sold':total_inProcess_sold,'total_complete_sold':total_complete_sold,'total_inStock_sold':total_inStock_sold,'count_sold_pending':count_sold_pending}
    return render(request, template_name, context)

def buyAProduct(request):
    #delete spam email
    spam=DeletedEmails.objects.all()
    for e in spam:
        Student.objects.filter(email=e.email).delete()
        User.objects.filter(email=e.email).delete()
    books=Book.objects.filter(status="verified")
    template_name="buyAProduct.html"
    context={"books":books}
    return render(request,template_name,context)

@login_required(login_url="login")
def sellAProduct(request):
    books=Book.objects.filter(seller__email__contains=request.user.username)
    template_name="sellAProduct.html"
    context={}
    return render(request,template_name,context)

@login_required(login_url="login")
def buyBook(request,bookId):
    customer=Student.objects.get(email=request.user.username)
    book=Book.objects.get(bookId=bookId)
    order_book_obj=Order_Book.objects.create(
        book=book,
        customer=customer
    )
    order_book_obj.save()
    status="inProcess"
    Book.objects.filter(bookId=bookId).update(status=status)
    print("timestamp: ",Order_Book.objects.get(book=book).timestamp)
    subject = 'Got a buyer for book ' + str(book.bookName)
    message = 'Someone has booked your book named ' + str(book.bookName) + '. Hurry up and check it asap!!!!'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [book.seller.email, ] 
    send_mail( subject, message, email_from, recipient_list )
    return redirect("orders")



@login_required(login_url="login")
def buySuit(request):
    if request.method == 'POST':
        customer=Student.objects.get(email=request.user.username)
        suit_gender=request.POST["suit-gender"]
        suit_size=request.POST["suit-size"]
        suit_condition=request.POST["suit-condition"]
        if(Suit.objects.filter(size=suit_size,gender=suit_gender,condition=suit_condition,status="inStock").exists()):
            suit1=Suit.objects.filter(size=suit_size,gender=suit_gender,condition=suit_condition,status="inStock")[0]
            suit_seller=suit1.seller.email
            Suit.objects.filter(seller__email__contains = suit_seller,size=suit_size,gender=suit_gender,condition=suit_condition,status="inStock").update(status="inProcess")
            suit_obj=Order_Suit(customer=customer,suit=suit1)
            suit_obj.save()
            return redirect("orders")
        else:
            template_name="unavailableProduct.html"
            return render(request,template_name)

@login_required(login_url="login")
def buyCoat(request):
    if request.method == 'POST':
        customer=Student.objects.get(email=request.user.username)
        coat_size=request.POST["coat-size"]
        coat_condition=request.POST["coat-condition"]
        if(Coat.objects.filter(size=coat_size, condition=coat_condition, status="inStock").exists()):
            coat1=Coat.objects.filter(size=coat_size, condition=coat_condition,status="inStock")[0]
            coat_seller=coat1.seller.email
            Coat.objects.filter(seller__email__contains = coat_seller,size=coat_size, condition=coat_condition,status="inStock").update(status="inProcess")
            coat_obj=Order_Coat(customer=customer, coat=coat1)
            coat_obj.save()
            return redirect("orders")
        else:
            template_name="unavailableProduct.html"
            return render(request,template_name)

@login_required(login_url="login")
def buyCalculator(request):
    if request.method == 'POST':
        customer=Student.objects.get(email=request.user.username)
        calculator_condition=request.POST["calculator-condition"]
        if(Calculator.objects.filter(condition=calculator_condition,status="inStock").exists()):
            calc1=Calculator.objects.filter(condition=calculator_condition,status="inStock")[0]
            calculator_seller=calc1.seller.email
            Calculator.objects.filter(seller__email__contains = calculator_seller, condition=calculator_condition,status="inStock").update(status="inProcess")
            calc_obj=Order_Calculator(customer=customer,calculator=calc1)
            calc_obj.save()
            return redirect("orders")
        else:
            template_name="unavailableProduct.html"
            return render(request,template_name)

@login_required(login_url="login")
def buyTool(request):
    if request.method == 'POST':
        customer=Student.objects.get(email=request.user.username)
        tool_obj=Order_Toolkit(customer=customer)
        tool_obj.save()
        return redirect("orders")


@login_required(login_url="login")
def sellBook(request):
    email=request.user.username
    student=Student.objects.get(email=email)
    if request.method == "POST" and request.FILES['book-image']:
        seller=student
        bookImage=request.FILES["book-image"]
        bookName=request.POST["book-name"]
        author=request.POST["book-author"]
        price=request.POST["book-price"]
        description=request.POST["book-description"]
        status="pending"
        book_obj=Book.objects.create(
            seller=seller,
            bookImage=bookImage,
            bookName=bookName,
            author=author,
            price=price,
            description=description,
            status=status
        )
        book_obj.save()
    return redirect("advertisements")

@login_required(login_url="login")
def sellSuit(request):
    email=request.user.username
    student=Student.objects.get(email=email)
    if request.method == "POST":
        suit_seller=student
        suit_description=request.POST["suit-description"]
        suit_size=request.POST["suit-size"]
        suit_gender=request.POST["suit-gender"]
        status="inStock"
        suit_obj=Suit.objects.create(
            seller=suit_seller,
            description=suit_description,
            status=status,
            size=suit_size,
            gender=suit_gender   
        )
        suit_obj.save()
    return redirect("advertisements")


@login_required(login_url="login")
def sellCoat(request):
    email=request.user.username
    student=Student.objects.get(email=email)
    if request.method == "POST":
        coat_seller=student
        coat_description=request.POST["coat-description"]
        coat_size=request.POST["coat-size"]
        status="inStock"
        coat_obj=Coat.objects.create(
            seller=coat_seller,
            description=coat_description,
            status=status,
            size=coat_size
        )
        coat_obj.save()
    return redirect("advertisements")

@login_required(login_url="login")
def sellCalculator(request):
    email=request.user.username
    student=Student.objects.get(email=email)
    if request.method == "POST":
        calc_seller=student
        status="inStock"
        calc_description=request.POST["calculator-description"]
        calc_obj=Calculator.objects.create(
            seller=calc_seller,
            status=status,
            description=calc_description
        )
        calc_obj.save()
    return redirect("advertisements")

@login_required(login_url="login")
def advertisements(request):
    email=request.user.username
    seller=Student.objects.get(email=email)
    books=Book.objects.filter(seller=seller)
    suits=Suit.objects.filter(seller=seller)
    coats=Coat.objects.filter(seller=seller)
    calculators=Calculator.objects.filter(seller=seller)
    context={'seller':seller,'books':books,'suits':suits,'coats':coats,'calculators':calculators}
    template_name="advertisements.html"
    return render(request, template_name, context)

@login_required(login_url="login")
def orders(request):
    email=request.user.username
    customer=Student.objects.get(email=email)
    orderedBooks=Order_Book.objects.filter(customer=customer)
    orderedSuits=Order_Suit.objects.filter(customer=customer)
    orderedCoats=Order_Coat.objects.filter(customer=customer)
    orderedCalculators=Order_Calculator.objects.filter(customer=customer)
    orderedToolkits=Order_Toolkit.objects.filter(customer=customer)
    context={'customer':customer,'orderedBooks':orderedBooks,'orderedSuits':orderedSuits, 'orderedCoats' :orderedCoats,'orderedCalculators':orderedCalculators,'orderedToolkits':orderedToolkits}
    template_name="orders.html"
    return render(request, template_name, context)




@login_required(login_url="login")
def deleteBook(request,bookId):
    seller=Student.objects.get(email=request.user.username)
    book= Book.objects.get(bookId=bookId)
    if((book.status=="verified" or book.status=="pending") and book.seller.email == request.user.username):
        Book.objects.filter(bookId=bookId).delete()
    return redirect("advertisements")


@login_required(login_url="login")
def deleteSuit(request,suitId):
    seller=Student.objects.get(email=request.user.username)
    suit= Suit.objects.get(suitId=suitId)
    if(suit.status=="inStock" and suit.seller.email == request.user.username):
        Suit.objects.filter(suitId=suitId).delete()
    return redirect("advertisements")

@login_required(login_url="login")
def deleteCoat(request,coatId):
    seller=Student.objects.get(email=request.user.username)
    coat= Coat.objects.get(coatId=coatId)
    if(coat.status=="inStock" and coat.seller.email == request.user.username):
        Coat.objects.filter(coatId=coatId).delete()
    return redirect("advertisements")
    
@login_required(login_url="login")
def deleteCalculator(request,calculatorId):
    seller=Student.objects.get(email=request.user.username)
    calculator= Calculator.objects.get(calculatorId=calculatorId)
    if(calculator.status=="inStock" and calculator.seller.email == request.user.username):
        Calculator.objects.filter(calculatorId=calculatorId).delete()
    return redirect("advertisements")


@login_required(login_url="login")
def completedBook(request,bookId,person):
    book=Book.objects.get(bookId=bookId)
    if(person=="seller"):
        if(book.status=="inProcess" and book.seller.email == request.user.username):
            Order_Book.objects.filter(book=book).update(flag_seller_complete=1)
            page="advertisements"
    if(person=="customer"):
        if(book.status=="inProcess" and book.order_books.customer.email == request.user.username):
            Order_Book.objects.filter(book=book).update(flag_customer_complete=1)
            page="orders"
    if(book.order_books.flag_seller_complete == '1' and Order_Book.objects.get(book=book).flag_customer_complete == '1'):
        status="sold"
        Book.objects.filter(bookId=bookId).update(status=status)
    return redirect(page)

@login_required(login_url="login")
def completedSuit(request,suitId,person):
    suit=Suit.objects.get(suitId=suitId)
    if(person=="seller"):
        if(suit.status=="inProcess" and suit.seller.email == request.user.username):
            Order_Suit.objects.filter(suit=suit).update(flag_seller_complete=1)
            page="advertisements"
    elif(person=="customer"):
        if(suit.status=="inProcess" and suit.order_suits.customer.email == request.user.username):
            Order_Suit.objects.filter(suit=suit).update(flag_customer_complete=1)
            page="orders"
    if(suit.order_suits.flag_seller_complete == '1' and Order_Suit.objects.get(suit=suit).flag_customer_complete == '1'):
        status="sold"
        Suit.objects.filter(suitId=suitId).update(status=status)
    return redirect(page)

@login_required(login_url="login")
def completedCoat(request,coatId,person):
    coat=Coat.objects.get(coatId=coatId)
    if(person=="seller"):
        if(coat.status=="inProcess" and coat.seller.email == request.user.username):
            Order_Coat.objects.filter(coat=coat).update(flag_seller_complete=1)
            page="advertisements"
    elif(person=="customer"):
        if(coat.status=="inProcess" and coat.order_coats.customer.email == request.user.username):
            Order_Coat.objects.filter(coat=coat).update(flag_customer_complete=1)
            page="orders"
    if(coat.order_coats.flag_seller_complete == '1' and Order_Coat.objects.get(coat=coat).flag_customer_complete == '1'):
        status="sold"
        Coat.objects.filter(coatId=coatId).update(status=status)
    return redirect(page)

@login_required(login_url="login")
def completedCalculator(request,calculatorId,person):
    calculator=Calculator.objects.get(calculatorId=calculatorId)
    if(person=="seller"):
        if(calculator.status=="inProcess" and calculator.seller.email == request.user.username):
            Order_Calculator.objects.filter(calculator=calculator).update(flag_seller_complete=1)
            page="advertisements"
    elif(person=="customer"):
        if(calculator.status=="inProcess" and calculator.order_calculators.customer.email == request.user.username):
            Order_Calculator.objects.filter(calculator=calculator).update(flag_customer_complete=1)
            page="orders"
    if(calculator.order_calculators.flag_seller_complete == '1' and  Order_Calculator.objects.get(calculator=calculator).flag_customer_complete== '1'):
        status="sold"
        Calculator.objects.filter(calculatorId=calculatorId).update(status=status)
    return redirect(page)


def tnc(request):
    return render(request,"termsandconditions.html")

def aboutUs(request):
    return render(request,"aboutUs.html")
    
'''def sellerSignUp(request):          
    context = {}
    if request.method == 'POST':
        s_form = SellerForm(request.POST)
        context['s_form'] = s_form
        print(context)
        if s_form.is_valid():
            print("Valid")

            username = s_form.cleaned_data.get('username')
            print(username)
            password = s_form.cleaned_data.get('Password')
            Email = s_form.cleaned_data.get('email')
            if User.objects.filter(email=Email).exists():
                print("Exist")
                messages.info(request, 'Email already exists')
                return HttpResponse('customer1')
            elif User.objects.filter(username=username).exists():
                print("Exist")
                messages.info(request, 'Username already exists')
                return HttpResponse('customer1')
            else:
                s_form.save()
                print("Saved")
                user = User.objects.create_user(username=username,password=password,email=Email)
                user.save()
                print('USerSaved')
            
                print("Done")
                
                return HttpResponse('customer1')
        else:
            return render(request, 'sellerSignUp.html', context)
    else:
        print("GET REQ")
        s_form = SellerForm()
        context['s_form'] = s_form
        return render(request, 'sellerSignUp.html', context)


def customerSignUp(request):          
    context = {}
    if request.method == 'POST':
        c_form = CustomerForm(request.POST)
        context['c_form'] = c_form
        print(context)
        if c_form.is_valid():
            print("Valid")

            username = c_form.cleaned_data.get('username')
            print(username)
            password = c_form.cleaned_data.get('Password')
            Email = c_form.cleaned_data.get('email')
            if User.objects.filter(email=Email).exists():
                print("Exist")
                messages.info(request, 'Email already exists')
                return HttpResponse('customer1')
            elif User.objects.filter(username=username).exists():
                print("Exist")
                messages.info(request, 'Username already exists')
                return HttpResponse('customer1')
            else:
                c_form.save()
                print("Saved")
                user = User.objects.create_user(username=username,password=password,email=Email)
                user.save()
                print('USerSaved')
            
                print("Done")
                
                return HttpResponse('customer1')
        else:
            return render(request, 'customerSignUp.html', context)
    else:
        print("GET REQ")
        c_form = CustomerForm()
        context['c_form'] = c_form
        return render(request, 'customerSignUp.html', context)


def login(request):
    if request.method=="POST":
        Username=request.POST.get('Username')
        Password=request.POST.get('Password')
        
        if Customer.objects.filter(username=Username,password=Password).exists() :
            user = User.objects.get(username=Username)
            auth.login(request,user)
            if request.GET.get("next",None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponse('Logged In !!!!!! ')

        elif Seller.objects.filter(username=Username,password=Password).exists():
            user = User.objects.get(username=Username)
            auth.login(request, user)
            if request.GET.get("next",None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponse("Logged In !!")
        
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')
'''

