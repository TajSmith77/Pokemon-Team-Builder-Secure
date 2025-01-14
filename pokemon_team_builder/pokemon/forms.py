from django import forms
from .models import *

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name',
            'pokemon1','ability1','move1_1','move1_2','move1_3','move1_4',
            'pokemon2','ability2','move2_1','move2_2','move2_3','move2_4',
            'pokemon3','ability3','move3_1','move3_2','move3_3','move3_4',
            'pokemon4','ability4','move4_1','move4_2','move4_3','move4_4',
            'pokemon5','ability5','move5_1','move5_2','move5_3','move5_4',
            'pokemon6','ability6','move6_1','move6_2','move6_3','move6_4', 'is_public']

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['name'].initial = instance.name
            self.fields['pokemon1'].initial = instance.pokemon1
            self.fields['ability1'].initial = instance.ability1
            self.fields['move1_1'].initial = instance.move1_1
            self.fields['move1_2'].initial = instance.move1_2
            self.fields['move1_3'].initial = instance.move1_3
            self.fields['move1_4'].initial = instance.move1_4
            self.fields['pokemon2'].initial = instance.pokemon2
            self.fields['ability2'].initial = instance.ability2
            self.fields['move2_1'].initial = instance.move2_1
            self.fields['move2_2'].initial = instance.move2_2
            self.fields['move2_3'].initial = instance.move2_3
            self.fields['move2_4'].initial = instance.move2_4
            self.fields['pokemon3'].initial = instance.pokemon3
            self.fields['ability3'].initial = instance.ability3
            self.fields['move3_1'].initial = instance.move3_1
            self.fields['move3_2'].initial = instance.move3_2
            self.fields['move3_3'].initial = instance.move3_3
            self.fields['move3_4'].initial = instance.move3_4
            self.fields['pokemon4'].initial = instance.pokemon4
            self.fields['ability4'].initial = instance.ability4
            self.fields['move4_1'].initial = instance.move4_1
            self.fields['move4_2'].initial = instance.move4_2
            self.fields['move4_3'].initial = instance.move4_3
            self.fields['move4_4'].initial = instance.move4_4
            self.fields['pokemon5'].initial = instance.pokemon5
            self.fields['ability5'].initial = instance.ability5
            self.fields['move5_1'].initial = instance.move5_1
            self.fields['move5_2'].initial = instance.move5_2
            self.fields['move5_3'].initial = instance.move5_3
            self.fields['move5_4'].initial = instance.move5_4
            self.fields['pokemon6'].initial = instance.pokemon6
            self.fields['ability6'].initial = instance.ability6
            self.fields['move6_1'].initial = instance.move6_1
            self.fields['move6_2'].initial = instance.move6_2
            self.fields['move6_3'].initial = instance.move6_3
            self.fields['move6_4'].initial = instance.move6_4
            self.fields['is_public'].initial = instance.is_public


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class MoveFilterForm(forms.Form):
    move_name = forms.ModelChoiceField(queryset=Move.objects.all(), required=False)
    move_type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False)
    min_damage = forms.IntegerField(required=False)
    