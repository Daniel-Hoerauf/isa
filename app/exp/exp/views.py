from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('Hello World\n')

def group(request):
    return HttpResponse('api group\n')

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Grouplist.objects.all()
    serializer_class = GrouplistSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()
