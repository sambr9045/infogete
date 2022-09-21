from . import views
from django.urls import path


urlpatterns = [
    path("", views.dashboard, name="home"),
    path("tickets", views.tickets, name="tickets"),
    path("ticket-details/<id>/", views.viewTicket, name="viewTicket"),
    path("contact-us", views.contactUs, name="contactUs"),
    path("tickets-list/<status>/", views.ticketList, name="ticketList"),
    path("suscription", views.suscriptions, name="suscriptions"),
    path("logout", views.logout, name="logout"),
    path("suscribe/<plan>/", views.suscribetoplan, name="plan"),
    path("payment/<uuid>/<plan>/", views.payment, name="payment"),
    path("profile", views.profile, name="profile"),
    path("change-password", views.changePassword, name="changepassword"),
    path("notification", views.n_notification, name="notification"),
    path("article/<uuid>/<title>/", views.viewarticle, name="viewarticle"),
    path("upgrade", views.upgradePlan, name="upgrade"),
    path("renew-plan", views.renew_plan, name="renewplan"),
    path("read-later", views.readLater, name="readlater"),
]
