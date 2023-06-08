from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for contact us view
     path(route='contact', view=views.contact, name='contact'),
    # path for registration
    path(route="registration/", view=views.registration_request, name='registration'),

    # path for login
 
    path(route='login/', view=views.login_request, name='login'),

    # path for logout
    path('logout', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='reviews/', view=views.get_dealer_details, name='reviews'),

    path(route='dealer/', view=views.get_dealer_id, name='dealer'),

    path(route='dealer/review/<int:id>/', view=views.get_dealer_review, name="dealer_details"),

    path(route='dealer/result/', view=views.search_dealer, name="search_result"),

    path(route='postreview/<int:id>/', view=views.post_review, name='post_review'),


   

    # path for add a review view


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)