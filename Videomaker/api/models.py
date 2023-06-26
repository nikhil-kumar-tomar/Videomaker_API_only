from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
# Create your models here.

class audio(models.Model):
    audio_file=models.FileField(upload_to="audio/")
    audio_name=models.CharField(max_length=400)
    start_time=models.IntegerField(default=0)
    end_time=models.IntegerField(default=0)
    date_time=models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return f"Audio Name={self.audio_name} ; Audio ID={self.id}"

class video(models.Model):
    video_file=models.FileField(upload_to="video/")
    video_name=models.CharField(max_length=400)
    start_time=models.IntegerField(default=0)
    end_time=models.IntegerField(default=0)
    date_time=models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"Video Name={self.video_name} ; Video ID={self.id}"


class audio_element(models.Model):
    choices=[
        ["vo","vo"],
        ["bg_music","bg_music"],
        ["video_music","video_music"],
    ]
    type=models.CharField(null=False,choices=choices,default="vo")
    volume=models.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0),
        ],null=True)
    url=models.URLField(null=True)
    start_time=models.IntegerField(default=0)
    end_time=models.IntegerField(default=0)
    audio_component_id=models.ForeignKey(audio,to_field="id",on_delete=models.CASCADE,null=True)
    video_component_id=models.ForeignKey(video,to_field="id",on_delete=models.CASCADE,null=True)
    date_time=models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"Audio Component={self.audio_component} ; Audio type={self.type}"
