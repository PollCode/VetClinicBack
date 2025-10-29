from rest_framework import serializers
from .models import Area

class AreaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Area
        fields = '__all__'
        
class AreaCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Area
        fields = ('name', 'description',)
