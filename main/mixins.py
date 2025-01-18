from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
    


class CustomLoginRequiredMixin(LoginRequiredMixin):


    permission_denied_message = "You need to login to view this page"


    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:

            messages.add_message(request, messages.WARNING,
                             self.permission_denied_message)
            return self.handle_no_permission()
        
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )