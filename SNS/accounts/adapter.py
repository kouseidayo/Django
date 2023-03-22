from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
  def save_user(self, request, user, form, commit):
    user = super().save_user(request, user, form, commit=False)
    user.age = form.cleaned_data.get("age")
    user.save()
