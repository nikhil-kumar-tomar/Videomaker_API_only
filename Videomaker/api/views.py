from rest_framework.views import Response,status,APIView
from rest_framework import generics
from .miscellaneous import object_all
from .serializers import *  
# Create your views here.

class get_audio_element(generics.RetrieveAPIView):
    queryset=object_all("audio_element")
    serializer_class=get_audio_element_serializer
    lookup_field="id"
    def get_object(self):
        id=self.kwargs["id"]
        return self.get_queryset().get(id=id)
    def get(self,request,*args, **kwargs):
            try:
                serializer_class=self.get_serializer(self.get_object())
                return Response(serializer_class.data,status=status.HTTP_200_OK)
            except:
                return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

class create_audio_element(generics.CreateAPIView):
    serializer_class=create_audio_element_serializer
    def post(self,request,*args, **kwargs):
        serializer_class=self.get_serializer(data=request.data)
        if serializer_class.is_valid():
            try:
                serializer_class.save()
            except Exception as e:
                return Response(e.args,status=status.HTTP_400_BAD_REQUEST) 
            return Response(serializer_class.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.error_messages,status.HTTP_400_BAD_REQUEST)





# Audio Upload created only for reference to other elements 
class audio_upload(APIView): # EXPERIMENTAL
    def post(self,request,*args, **kwargs):
        serializer_class=audio_serializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data,status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,*args, **kwargs):
        queryset=object_all("audio")
        serializer_class=audio_serializer(queryset,many=True)
        return Response(serializer_class.data,status=status.HTTP_200_OK)

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
