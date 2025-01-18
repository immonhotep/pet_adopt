from .models import UserProfile,UserMessage


def  navbar_context(request):
    
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

        unanswered = UserMessage.objects.filter(receiver=request.user, replied=False)
         

    else:
        profile={}
        unanswered = {}
  
    return {'profile':profile,'unanswered':unanswered}