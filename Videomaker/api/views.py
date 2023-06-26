from rest_framework.views import Response,status,APIView
from rest_framework import generics
from .miscellaneous import object_all
from .serializers import *  
# Create your views here.

# Read Information from audio element
class get_audio_element(generics.RetrieveAPIView):
    queryset=object_all("audio_element")
    serializer_class=get_audio_element_serializer
    lookup_field="id"
    def get_object(self):
        id=self.kwargs["id"]
        return self.get_queryset().get(id=id)
    def get(self,request,*args, **kwargs):
            try:
                serializer=self.get_serializer(self.get_object())
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

# Create audio elements
class create_audio_element(generics.CreateAPIView):
    serializer_class=create_audio_element_serializer
    def post(self,request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response(e.args,status=status.HTTP_400_BAD_REQUEST) 
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages,status.HTTP_400_BAD_REQUEST)

# Delete audio elements
class delete_audio_element(generics.DestroyAPIView):
    queryset=object_all("audio_element")
    serializer_class=get_audio_element_serializer
    lookup_field='id'
    def delete(self,request,*args, **kwargs):
        instance=self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response("Data Deleted Successfully",status=status.HTTP_200_OK)
        else:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

# Update audio elements
class update_audio_element(generics.UpdateAPIView):
    queryset=object_all("audio_element")
    serializer_class=update_audio_element_serializer
    lookup_field='id'
    def update(self, request, *args, **kwargs):
        instance=self.get_object()
        if instance:
            serializer=self.get_serializer(instance,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)


# API's below are not asked in the assignment, They are created purely for more functionality.
# Audio Upload created only for reference to other elements 
class audio_upload(APIView): # EXPERIMENTAL
    def post(self,request,*args, **kwargs):
        serializer=audio_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response(e.args,status=status.HTTP_400_BAD_REQUEST) 
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,*args, **kwargs):
        queryset=object_all("audio")
        serializer=audio_serializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

# Video Upload created only for reference to other elements
class video_upload(APIView): # EXPERIMENTAL
    def post(self,request,*args, **kwargs):
        serializer_class=video_serializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data,status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,*args, **kwargs):
        queryset=object_all("video")
        serializer_class=video_serializer(queryset,many=True)
        return Response(serializer_class.data,status=status.HTTP_200_OK)
