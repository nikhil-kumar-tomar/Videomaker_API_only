# Videomaker_API_only
This is a Videomaker project and only consists of API for the platform, It consists of 7 API's out of which 5 are necessary for CRUD operations and applying business logic whereas as 2 are added as experimental API for better performance.

# Working

The working of all API's is straightforward and according to the rules. 
I am going to define the API's Below:

### Note:

To utilize any API just use the link [URL of the website]/api/[Name of APi]/[parameters if any]/

For all cases below I am going to take URL of websites as `localhost` this can change and depends on where is the web app deplyoyed

*The easiest and recommended way to check all of these apis is directly accessing them using a web browser a beautifll interface will be shown to interact with apis in a graphical manner, Although software like postman can also be used depending on the choice of the user*

## Get Audio Element

This is a api to get the information for the already saved audio elements in the database:

Link: localhost/api/get_audio_element/[int:id]/

Also, Get required a `GET` http method to be executed

id is supposed to be passed by the user, this API will return a lot of information about the element which will contain information from URL,volume,duration and more.
example is below:

Accessed Link: http://localhost:8000/api/get_audio_element/65/

```json
{
    "id": 65,
    "type": "bg_music",
    "volume": 75,
    "url": "audio/Initial_D_-_All_Around.mp3",
    "audio_component_id": 7,
    "video_component_id": null,
    "duration": {
        "start_time": 10,
        "end_time": 40
    }
}
```

## Create Audio Element

This api is for creating a audio element and follows a lot of rules, listed below

1. Same audio types are not overlapped and are appended one after another
2. For video_audio or video_music the duration is required to be filled by the user but it is filled at server side only, and is taken from the video's start and end duration.

Link: localhost/api/create_audio_element/

It is required to fill data in for this api in format, example is below

Also, Create required a `POST` http method to be executed

Accessed Link: http://localhost:8000/api/create_audio_element/
```json
{
    "type":"vo",
    "start_time": 15,
    "end_time": 25,
    "audio_component_id":7,
    "video_component_id":null
}
```

in the above type: can only have 3 choices:
+ "vo" for voice over
+ "bg_music" for background music
+ "video_music" for video music

also audio_component_id and video_component_id are foreign keys from actually uploaded audios and videos and therefore require their specific ids otherwise the api will throw errors.

Again to be efficient use web browser and copy paste the link directly on web page to interact it is very effiecient

The return JSON from above request will be
```json
{
    "id": 71,
    "url": "audio/Initial_D_-_All_Around.mp3",
    "type": "vo",
    "audio_component_id": 7,
    "video_component_id": null,
    "duration": {
        "start_time": 20,
        "end_time": 30
    }
}
```
As you can see the start_time a got affected automatically and shifted our time start_time to 20 this means another audio element of type vo was present in the database whoose ending time was 20.

## Delete Audio Element

It is simple api to delete a Audio Element

Link: localhost/api/delete_audio_element/[int:id]/

Also, Delete required a `DELETE` http method to be executed

example is below:

Accessed Link: http://localhost:8000/api/delete_audio_element/71/

Return of API

```json
"Data Deleted Successfully"
```

## Update Audio Element

Update audio element is for updating existing audio elements it has been proposed with various limitations to keep its behaviour strict.

Rules are list below:
+ Audio_component_id and Video_Component_id cannot be selected together
+ If type is non Video type only Audio_Component_id is filled and Video_component_is is null and vice versa
+ If type is video_music changing its video_component_id is not allowed(Required) 

Link: localhost/api/update_audio_element/[int:id]/

Also, Delete required a `PUT` http method to be executed
example is below:

Accessed Link: http://localhost:8000/api/update_audio_element/72/

Database Information of audio element of id 72:
```json
{
    "id": 72,
    "type": "bg_music",
    "volume": 25,
    "url": "audio/Initial_D_-_All_Around.mp3",
    "audio_component_id": 7,
    "video_component_id": null,
    "duration": {
        "start_time": 15,
        "end_time": 25
    }
}
```

Given information for update:
```json
{
    "type":"vo",
    "start_time": 5,
    "end_time": 15,
    "audio_component_id":7,
    "video_component_id":null
}
```

Return Information:
```json
{
    "id": 72,
    "type": "vo",
    "volume": 50,
    "url": "audio/Initial_D_-_All_Around.mp3",
    "audio_component_id": 7,
    "video_component_id": null,
    "duration": {
        "start_time": 15,
        "end_time": 25
    }
}
```

## Get Audio Fragments

This API return information for all the audio fragments in the given time interval


Link: localhost/api/get_audio_fragments/

Also, This required a `POST` http method to be executed

This API requires 2 inputs start_time and end_time which defines the interval in which audio fragments are required.

example is below:
Accessed link: http://localhost:8000/api/get_audio_fragments/

Given Information:
```json
{
    "start_time": 0,
    "end_time": 30
}
```
return

```json
{
    "fragments": [
        {
            "id": 73,
            "type": "vo",
            "url": "audio/Initial_D_-_All_Around.mp3",
            "volume": 100,
            "duration": {
                "start_time": 5,
                "end_time": 10
            },
            "audio_component_id": 7,
            "video_component_id": null
        },
        {
            "id": 73,
            "type": "vo",
            "url": "audio/Initial_D_-_All_Around.mp3",
            "volume": 75,
            "duration": {
                "start_time": 10,
                "end_time": 20
            },
            "audio_component_id": 7,
            "video_component_id": null
        },
        {
            "id": 74,
            "type": "bg_music",
            "url": "audio/Initial_D_-_All_Around.mp3",
            "volume": 50,
            "duration": {
                "start_time": 10,
                "end_time": 25
            },
            "audio_component_id": 7,
            "video_component_id": null
        },
        {
            "id": 74,
            "type": "bg_music",
            "url": "audio/Initial_D_-_All_Around.mp3",
            "volume": 100,
            "duration": {
                "start_time": 25,
                "end_time": 30
            },
            "audio_component_id": 7,
            "video_component_id": null
        },
        {
            "id": 75,
            "type": "video_music",
            "url": "video/pexels-pixabay-855289-1920x1080-25fps.mp4",
            "volume": 25,
            "duration": {
                "start_time": 15,
                "end_time": 25
            },
            "audio_component_id": null,
            "video_component_id": 4
        }
    ]
}

```

# Experimental API. 

Most of the API's above require a Foreign Key in form of audio_component_id and video_component_id and these foreign keys are mapped to the id of the audio and video upload tables in database.

There are only 2 Experimental API for uploading audio and video to the application listed below  .

## Audio Upload API

This API is used to upload Audio to our application
Link: localhost/api/upload_audio/

It required Input list below:

1. start_time
2. end_time
3. audio_file
4. audio_name

These information can be filled directly from the web browser or postman app using paramters body and form-data which gives a key value pair from their even file upload is possible.

example Return:

```json
{
    "id": 10,
    "audio_file": "/media/audio/Initial_D_-_All_Around.mp3",
    "audio_name": "Some_Audio",
    "date_time": "2023-06-28T17:33:20.444312+05:30",
    "duration": {
        "start_time": 0,
        "end_time": 90
    }
}

```

## Video Upload API

This API is similar to Audio upload API, instead it is used to upload videos rather than audios to our web applicatoin.

Link: localhost/api/upload_video/

Required Inputs:
1. start_time
2. end_time
3. video_file
4. video_name

These information is again recommended to be filled using Web Browser interface

example Return
```json
{
    "id": 1,
    "video_file": "/media/video/pexels-pixabay-855289-1920x1080-25fps.mp4",
    "video_name": "Some",
    "date_time": "2023-06-27T00:49:54.443681+05:30",
    "duration": {
        "start_time": 0,
        "end_time": 106
    }
}
```

