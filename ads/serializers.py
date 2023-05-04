from rest_framework.fields import BooleanField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Ad, Compilation, Category
from ads.validators import check_is_published
from users.models import User


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(ModelSerializer):
    author_id = SlugRelatedField(slug_field='id', queryset=User.objects.all())
    category_id = SlugRelatedField(slug_field='id', queryset=Category.objects.all())
    is_published = BooleanField(validators=[check_is_published], required=False)

    class Meta:
        model = Ad
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class CompilationSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Compilation


class CompilationRetrieveSerializer(ModelSerializer):
    items = AdSerializer(many=True)

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
