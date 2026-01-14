from rest_framework import serializers
from .models import Area, Breed

class AreaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Area
        fields = '__all__'
        
class AreaRelateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Area
        fields = ('id', 'name')
        
class AreaCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Area
        fields = ('name', 'description',)

        
class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'
        
class BreedRelateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Breed
        fields = ('id', 'name',)
        
class BreedCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Breed
        fields = ('name', 'species', 'size_category')

        