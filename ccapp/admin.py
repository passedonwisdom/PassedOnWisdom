from django.contrib import admin
from .models import Student, Book, Suit, Coat, Calculator, Order_Book,Order_Suit, Order_Coat, Order_Calculator, Order_Toolkit, Report_Book, Feedback,DeletedEmails
# Register your models here.

admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Suit)
admin.site.register(Coat)
admin.site.register(Calculator)
admin.site.register(Order_Book)
admin.site.register(Order_Suit)
admin.site.register(Order_Coat)
admin.site.register(Order_Calculator)
admin.site.register(Order_Toolkit)
admin.site.register(Report_Book)
admin.site.register(Feedback)
admin.site.register(DeletedEmails)