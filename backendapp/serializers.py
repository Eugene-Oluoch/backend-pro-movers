from rest_framework import serializers

from backendapp.models import User, Request, Mover, RegUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        acc_type = validated_data['acc_type']
        if acc_type == 'mover':
            mover = Mover(
                user=user,
                company_name=validated_data['name']
            )
            mover.save()
        else:
            reguser = RegUser(
                user=user,
                full_name=validated_data['name']
            )
            reguser.save()
        # user.update({"acc_type": acc_type})
        return user


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('currentLocation','newLocation','created','id_user','id_mover','user','mover','fees','Package','is_accepted','is_pending','is_declined','packageDescription','movingDate')
        


class RegUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegUser
        fields = "__all__"
        read_only_fields = ['user']


class MoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mover
        fields = '__all__'
        read_only_fields = ['user']
