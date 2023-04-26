from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Ad, Compilation
from users.models import User


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class CompilationSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Compilation


class CompilationListSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        fields = ['owner', 'name']
        model = Compilation


class CompilationCreateSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field='username', read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        fields = ['owner', 'name']
        model = Compilation
