from rest_framework import serializers
from django.contrib.auth.models import User
from .models import audio_element,audio,video
from .business_logic import server_postfill
from .miscellaneous import object_creator
from django.core.exceptions import ValidationError,BadRequest

class get_audio_element_serializer(serializers.ModelSerializer):
    class Meta:
        model=audio_element
        fields=['id','type','volume','url','start_time','end_time','audio_component_id','video_component_id']
    def to_representation(self, instance):
        representation= super().to_representation(instance)
        representation["duration"]={"start_time":representation["start_time"],"end_time":representation["end_time"]}
        del representation['start_time']
        del representation['end_time']
        return representation

class create_audio_element_serializer(serializers.ModelSerializer):
    start_time=serializers._(required=True)
    end_time=serializers._(required=True)
    type=serializers._
    class Meta:
        model=audio_element
        fields=['id','url','type','start_time','end_time','audio_component_id','video_component_id']
        read_only_fields=['id','url']
    def create(self, validated_data):
        validated_data=server_postfill(validated_data)
        server_updated={
            'type':validated_data['type'],
            'volume':100, # Currently(Make Logic)
            'url':validated_data["url"],
            'start_time':validated_data['start_time'],
            'end_time':validated_data['end_time'],
            'audio_component_id':validated_data['audio_component_id'],
            'video_component_id':validated_data['video_component_id']
        }
        return object_creator(server_updated,"audio_element")    
    def to_representation(self, instance):
        representation= super().to_representation(instance)
        representation["duration"]={"start_time":representation["start_time"],"end_time":representation["end_time"]}
        del representation['start_time']
        del representation['end_time']
        return representation


class audio_serializer(serializers.ModelSerializer):
    start_time=serializers.IntegerField(required=True)
    end_time=serializers.IntegerField(required=True)
    audio_file=serializers.FileField()
    def validate_audio_file(self,audio_file):
        if audio_file.content_type[0:5]!="audio":
            raise ValidationError("Wrong File Format Uploaded")
        return audio_file
    class Meta:
        model=audio
        fields='__all__'

class video_serializer(serializers.ModelSerializer):
    start_time=serializers.IntegerField(required=True)
    end_time=serializers.IntegerField(required=True)
    video_file=serializers.FileField()
    def validate_video_file(self,video_file):
        if video_file.content_type[0:5]!="video":
            raise ValidationError("Wrong File Format Uploaded")
        return video_file
    class Meta:
        model=video
        fields='__all__'