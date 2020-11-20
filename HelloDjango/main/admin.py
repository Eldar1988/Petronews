from django.contrib import admin
from .models import MainInfo, Contacts, Social, Footer, Politic, About, TgBot

admin.site.register(MainInfo)
admin.site.register(TgBot)
admin.site.register(Contacts)
admin.site.register(Social)
admin.site.register(Footer)
admin.site.register(Politic)
admin.site.register(About)
