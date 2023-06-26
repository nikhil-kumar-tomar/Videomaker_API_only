from .miscellaneous import object_get,object_exists,object_all_order_by,object_filter_orderby
from django.core.exceptions import BadRequest


def is_overlap(all_objects:object,target_object:object)->object:
    overlap=False
    element=target_object
    for elements in all_objects:
        if (target_object["start_time"] <= elements.start_time and target_object["end_time"]<=elements.start_time) or (target_object["start_time"] >= elements.end_time and target_object["end_time"]>=elements.end_time):
            # Not overlapping data
            pass
        else:
            # Overlapping data
            overlap=True
            element=elements
    return [overlap,element]

def overlap_check_volume(validated_data:dict)->int:
    """
    Function to Check overlaps between new elements and database elements
    """
    volume=validated_data["volume"]
    is_over=is_overlap(object_all_order_by("audio_element","-volume"),validated_data)
    if is_over[0]:
        volume=is_over[1].volume-25
    return volume


def server_postfill(validated_data:dict)->dict:
    """
    Function to Postfill the entries according to the business logic
    """
    
    if not(validated_data["audio_component_id"] and validated_data["video_component_id"]):
        if validated_data["audio_component_id"] and validated_data["type"]!="video_music":
            validated_data["url"]=object_get({"id":validated_data["audio_component_id"].id},"audio").audio_file
            if object_exists({"type":validated_data["type"]},"audio_element"):
                is_over=is_overlap([object_filter_orderby({"type":validated_data["type"]},"audio_element","-date_time")[0]],validated_data)
                if is_over[0]:
                    temp_time=is_over[1].end_time-validated_data["start_time"]
                    validated_data["start_time"]+=temp_time
                    validated_data["end_time"]+=temp_time
            validated_data["volume"]=overlap_check_volume(validated_data)
            
        elif validated_data["video_component_id"] and validated_data["type"]=="video_music":
            validated_data["url"]=object_get({"id":validated_data["video_component_id"].id},"video").video_file
            validated_data["start_time"]=object_get({"id":validated_data["video_component_id"].id},"video").start_time
            validated_data["end_time"]=object_get({"id":validated_data["video_component_id"].id},"video").end_time
            if object_exists({"type":validated_data["type"]},"audio_element"):
                is_over=is_overlap([object_filter_orderby({"type":validated_data["type"]},"audio_element","-date_time")[0]],validated_data)
                if is_over[0]:
                    temp_time=is_over[1].end_time-validated_data["start_time"]
                    validated_data["start_time"]+=temp_time
                    validated_data["end_time"]+=temp_time
            validated_data["volume"]=overlap_check_volume(validated_data)

        else:
            raise BadRequest("Bad Input Selected")
        return validated_data    
    else:
        raise BadRequest("Bad Input Selected")





