from django.db import models
from django.contrib.auth.models import User

class Ability(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Move(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    power = models.IntegerField(null=True)
    pp = models.IntegerField(null=True)
    accuracy = models.IntegerField(null=True)
   
    def __str__(self):
        return self.name
    
class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    types = models.ManyToManyField(Type)
    held_item = models.TextField(null=True)
    hp = models.IntegerField(null=True)
    attack = models.IntegerField(null=True)
    defense = models.IntegerField(null=True)
    special_attack = models.IntegerField(null=True)
    special_defense = models.IntegerField(null=True)
    speed = models.IntegerField(null=True)
    abilities = models.ManyToManyField(Ability)
    sprites = models.URLField()
    moves = models.ManyToManyField(Move)
    
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon1 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon1')
    ability1 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability1', null=True)
    move1_1 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move1_1', null=True)
    move1_2 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move1_2', null=True)
    move1_3 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move1_3', null=True)
    move1_4 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move1_4', null=True)
    pokemon2 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon2')
    ability2 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability2', null=True)
    move2_1 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move2_1', null=True)
    move2_2 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move2_2', null=True)
    move2_3 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move2_3', null=True)
    move2_4 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move2_4', null=True)
    pokemon3 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon3')
    ability3 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability3', null=True)
    move3_1 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move3_1', null=True)
    move3_2 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move3_2', null=True)
    move3_3 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move3_3', null=True)
    move3_4 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move3_4', null=True)
    pokemon4 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon4')
    ability4 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability4', null=True)
    move4_1 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move4_1', null=True)
    move4_2 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move4_2', null=True)
    move4_3 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move4_3', null=True)
    move4_4 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move4_4', null=True)
    pokemon5 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon5')
    ability5 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability5', null=True)
    move5_1 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move5_1', null=True)
    move5_2 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move5_2', null=True)
    move5_3 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move5_3', null=True)
    move5_4 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move5_4', null=True)
    pokemon6 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon6')
    ability6 = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='ability6', null=True)
    move6_1 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move6_1', null=True)
    move6_2 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move6_2', null=True)
    move6_3 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move6_3', null=True)
    move6_4 = models.ForeignKey(Move, on_delete=models.CASCADE, related_name='move6_4', null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name