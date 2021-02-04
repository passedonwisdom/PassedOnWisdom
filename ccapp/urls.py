from django.urls import path
from . import views,urls
from django.conf import settings


urlpatterns = [
    path('', views.index,name="index"),
    #path('sellerSignUp',views.sellerSignUp , name="sellerSignUp" ),
    #path('customerSignUp',views.customerSignUp , name="customerSignUp" ) ,
    path('login' , views.login , name="login"),
    path('logout' , views.logout , name="logout"),
    path('signup',views.signup,name="signup"),
    path('profile',views.profile,name="profile"),
    path('buyAProduct',views.buyAProduct,name="buyAProduct"),
    path('sellAProduct',views.sellAProduct,name="sellAProduct"),
    path('buyBook/<int:bookId>',views.buyBook,name="buyBook"),
    path('buySuit',views.buySuit,name="buySuit"),
    path('buyCoat',views.buyCoat,name="buyCoat"),
    path('buyCalculator',views.buyCalculator,name="buyCalculator"),
    path('buyTool',views.buyTool,name="buyTool"),
    path('sellBook',views.sellBook,name="sellBook"),
    path('sellSuit',views.sellSuit,name="sellSuit"),
    path('sellCoat',views.sellCoat,name="sellCoat"),
    path('sellCalculator',views.sellCalculator,name="sellCalculator"),
    path('advertisements',views.advertisements,name="advertisements"),
    path('orders',views.orders,name="orders"),
    path('deleteBook/<int:bookId>',views.deleteBook,name="deleteBook"),
    path('deleteSuit/<int:suitId>',views.deleteSuit,name="deleteSuit"),
    path('deleteCoat/<int:coatId>',views.deleteCoat,name="deleteCoat"),
    path('deleteCalculator/<int:calculatorId>',views.deleteCalculator,name="deleteCalculator"),
    path('completedBook/<int:bookId>/<str:person>',views.completedBook,name="completedBook"),
    path('completedSuit/<int:suitId>/<str:person>',views.completedSuit,name="completedSuit"),
    path('completedCoat/<int:coatId>/<str:person>',views.completedCoat,name="completedCoat"),
    path('completedCalculator/<int:calculatorId>/<str:person>',views.completedCalculator,name="completedCalculator"),
    path('termsandconditions',views.tnc,name="tnc"),
    path('aboutUs',views.aboutUs,name="aboutUs"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)