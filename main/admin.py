from django.contrib import admin
from .models import UserProfile,PetCategory,Pet,ContactMessage,ContactMessageAnswer,Adoptation,UserMessage,ReplyUserMessage

admin.site.register(UserProfile)
admin.site.register(PetCategory)
admin.site.register(Pet)
admin.site.register(ContactMessage)
admin.site.register(ContactMessageAnswer)
admin.site.register(Adoptation)
admin.site.register(UserMessage)
admin.site.register(ReplyUserMessage)
