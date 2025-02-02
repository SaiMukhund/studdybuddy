from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):

    class Meta:
        model=Room
        fields='__all__' #["name","description"]
        exclude=["host","participants"]