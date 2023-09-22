from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model


class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        required=False  # Allow supporter to be null
    )

    class Meta:
        model = apps.get_model("projects.Pledge")
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = apps.get_model("projects.Project")
        fields = "__all__"


class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        if instance.is_open:
            instance.title = validated_data.get("title", instance.title)
            instance.description = validated_data.get(
                "description",
            )
            instance.goal = validated_data.get("goal", instance.goal)
            instance.image = validated_data.get("image", instance.image)
            instance.is_open = validated_data.get("is_open", instance.is_open)
            instance.date_created = validated_data.get(
                "date_created", instance.date_created
            )
            instance.is_deleted = validated_data.get("is_deleted", instance.is_deleted)
            if instance.is_deleted == True:
                instance.is_open = False
                for pledge in instance.pledges.all():
                    pledge.is_deleted = True
                pledge.save()
                instance.save()
            else:
                instance.is_open = validated_data.get("is_open", instance.is_open)
                instance.is_deleted = validated_data.get(
                    "is_deleted", instance.is_deleted
                )
                instance.save()
        return instance
