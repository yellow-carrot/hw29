from rest_framework.serializers import ModelSerializer, SlugRelatedField, IntegerField

from users.models import Location, User


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


# ----------------------------------User_Serializers:-------------------------


class UserListSerializer(ModelSerializer):
    locations = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ['location_id']


class UserRetrieveSerializer(ModelSerializer):
    locations = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(ModelSerializer):
    id = IntegerField(required=False)
    location_id = SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='id'
    )

    def is_valid(self, raise_exception=False):
        self._location_id = self.initial_data.pop("locations")
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._location_id:
            obj, _ = Location.objects.get_or_create(name=location)
            user.location_id.add(obj)

        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'