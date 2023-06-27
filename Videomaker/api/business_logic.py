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


def update_server_postfill(validated_data:dict,instance:dict)->dict:
    """
    Function to Postfill the entries according to the business logic for update
    """
    is_over=is_overlap(object_all_order_by("audio_element","-volume"),validated_data)
    if validated_data["type"]!="video_music" and (not(is_over[0]) or instance.type=="video_music"):
        # start and end time will only change if data is not overlapping
        instance.start_time=validated_data["start_time"]
        instance.end_time=validated_data["end_time"]  
    if validated_data["type"]!="video_music": # Changes only if type of music is not video_music
        if instance.video_component_id:
            instance.video_component_id=None
            instance.url=None
        if validated_data["type"]!=instance.type:
            instance.type=validated_data["type"]
        if validated_data["audio_component_id"]!=instance.audio_component_id:
            instance.audio_component_id=validated_data["audio_component_id"]
            instance.url=object_get({"id":validated_data["audio_component_id"].id},"audio").audio_file
    elif validated_data["type"]=="video_music": # Changes only if type of music is  video_music
        inst_obj=object_get({"id":validated_data["video_component_id"].id},"video")
        instance.start_time=validated_data["start_time"]=inst_obj.start_time
        instance.end_time=validated_data["end_time"]=inst_obj.end_time
        if instance.audio_component_id:
            instance.audio_component_id=None
            instance.url=None
        if validated_data["type"]!=instance.type:
            instance.type=validated_data["type"]
        if validated_data["video_component_id"]!=instance.video_component_id:
            instance.video_component_id=validated_data["video_component_id"]
            instance.url=inst_obj.video_file
        # Checking for overlaps
        if object_exists({"type":validated_data["type"]},"audio_element") and object_filter_orderby({"type":validated_data["type"]},"audio_element","date_time")[0].id!=instance.id:
            is_over=is_overlap([object_filter_orderby({"type":validated_data["type"]},"audio_element","date_time")[0]],validated_data)
            if is_over[0]:
                temp_time=is_over[1].end_time-validated_data["start_time"]
                validated_data["start_time"]+=temp_time
                validated_data["end_time"]+=temp_time
                instance.start_time=validated_data["start_time"]
                instance.end_time+=validated_data["end_time"]
    validated_data["volume"]=100
    instance.volume=overlap_check_volume(validated_data)
    # Note: Volume,url are set by server and therefore cannot be changed by the user    
    return instance


def call_obj_fragment(start_time:int,end_time:int)->list:
    """
    Call Objects and modify them according to the required needs
    """
    all_objects=object_filter_orderby({"start_time__gte":start_time},"audio_element","start_time")

    for obj in all_objects:
        if obj.end_time>end_time:
            obj.end_time=end_time
    return all_objects

def dictionary_filler(x:dict,start_time:int,end_time:int,volume)->dict:
    """
    x is default objects which are being itetrated everything else is obvious
    Simple function to make everything a little beautiful and follow DRY principle alongside
    """
    temp={
            'id':x.id,
            "type":x.type,
            "url":x.url,
            "volume":volume,
            "duration":{
        "start_time":start_time,
        "end_time":end_time
            }
        }
    if x.audio_component_id:
        temp["audio_component_id"]=x.audio_component_id_id
    else:
        temp["audio_component_id"]=None
    if x.video_component_id:
        temp["video_component_id"]=x.video_component_id_id
    else:
        temp["video_component_id"]=None

    return temp

def make_fragments(start_time:int,end_time:int)->list:
    """
    Make Fragments of Audio(Contains Logic )
    """
    representation=[]
    all_objects=call_obj_fragment(start_time,end_time)
    prev_lowest_end_time=[0]
    shared_overlapping_volume=100
    for x in all_objects:
        prev_end_time=prev_lowest_end_time[len(prev_lowest_end_time)-1]# lowest prev number
        other_than_current_objects=[y for y in all_objects if y!=x]
        start_times=[em.start_time for em in other_than_current_objects]
        end_times=[em.end_time for em in other_than_current_objects]
        main_lis=[em for em in start_times if em<x.end_time and em>x.start_time]+[em for em in end_times if em<x.end_time and em>x.start_time]
        if len(main_lis)>1:
            main_lis=[em for em in main_lis if em>prev_end_time and em not in prev_lowest_end_time]
            frag_element=min(main_lis)
        elif len(main_lis)==1:
            frag_element=main_lis[0]
        else:
            shared_overlapping_volume-=25
            representation.append(dictionary_filler(x,x.start_time,x.end_time,shared_overlapping_volume))
            continue
        if ([temp for temp in end_times if frag_element<temp]) and not([temp for temp in start_times if frag_element>temp]):
            representation.append(dictionary_filler(x,x.start_time,frag_element,100))# non-overlapping
            shared_overlapping_volume-=25
            representation.append(dictionary_filler(x,frag_element,x.end_time,shared_overlapping_volume)) # overlapping
        if not([temp for temp in end_times if frag_element<temp]) and ([temp for temp in start_times if frag_element>temp]):
            shared_overlapping_volume-=25
            representation.append(dictionary_filler(x,x.start_time,frag_element,shared_overlapping_volume)) # overlapping
            representation.append(dictionary_filler(x,frag_element,x.end_time,100)) # non-overlapping
        if ([temp for temp in end_times if frag_element<temp]) and ([temp for temp in start_times if frag_element>temp]):
            shared_overlapping_volume-=25
            representation.append(dictionary_filler(x,x.start_time,x.end_time,shared_overlapping_volume)) # overlapping
        
        prev_lowest_end_time.append(x.end_time)
    return representation