from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):

  def __init__(self, *args, **kwargs): # emailの登録を必須に変更
      super().__init__(*args, **kwargs)
      self.fields["email"].required = True

  class Meta:
    model = get_user_model()
    fields = ["username", "email", "age"] # passwordは設定しない
    labels = {
      "username": "ユーザー名",
      "email": "メールアドレス",
      "age": "年齢",
    }
    help_texts = {
      "username": "",
      "email": "",
      "age": "",
    }

class CustomUserChangeForm(UserChangeForm):
  def __init__(self, *args, **kwargs): # emailの登録を必須に変更
      super().__init__(*args, **kwargs)
      self.fields["email"].required = True

  class Meta:
    model = get_user_model()
    fields = ["username", "email", "age"] # passwordは設定しない
    labels = {
      "username": "ユーザー名",
      "email": "メールアドレス",
      "age": "年齢",
    }
    help_texts = {
      "username": "",
      "email": "",
      "age": "",
    }
