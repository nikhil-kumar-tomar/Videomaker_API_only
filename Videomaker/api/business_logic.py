from .miscellaneous import object_get
from django.core.exceptions import BadRequest
def server_postfill(validated_data:dict)->dict:
    """
    Function to find the default url for audio_elements
    """
    
    if not(validated_data["audio_component_id"] and validated_data["video_component_id"]):
        if validated_data["audio_component_id"] and validated_data["type"]!="video_music":
            validated_data["url"]=object_get({"id":validated_data["audio_component_id"].id},"audio").audio_file
            
        elif validated_data["video_component_id"] and validated_data["type"]=="video_music":
            validated_data["url"]=object_get({"id":validated_data["video_component_id"].id},"video").video_file
            validated_data["start_time"]=object_get({"id":validated_data["video_component_id"].id},"video").start_time
            validated_data["end_time"]=object_get({"id":validated_data["video_component_id"].id},"video").end_time
        else:
            raise BadRequest("Bad Input Selected")
        return validated_data    
    else:
        raise BadRequest("Bad Input Selected")





