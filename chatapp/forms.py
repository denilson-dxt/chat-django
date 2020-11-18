from django import forms
from .models import User
from cloudinary.forms import CloudinaryJsFileField


class ChangePerfilPictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("perfil_picture", )
