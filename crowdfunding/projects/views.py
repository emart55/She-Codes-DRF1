from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer
from django.http import Http404
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly
import pdb

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, is_deleted=False, is_open=True)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            # projects = Project.objects.all().filter(is_deleted=False)
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            instance=project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# class PledgeList(APIView):

#     def get(self, request):
#         pledges = Pledge.objects.all().filter(is_deleted=False)
#         serializer = PledgeSerializer(pledges,many=True)
#         return Response(serializer.data)
    
#     def post(self, request, pk):
#         pledge = request.data
#         project_id = pledge.get('project')

#         if project_id is None:
#             return Response(
#                 {'error': 'The "project" field is required.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             project = Project.objects.get(pk=project_id)
#         except Project.DoesNotExist:
#             return Response(
#                 {'error': 'The specified project does not exist.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = PledgeSerializer(data=request.data)
#         if project.is_open == True:
#             if serializer.is_valid():
#                 serializer.save(supporter=request.user, is_deleted=False)
#                 return Response(
#                     serializer.data,
#                     status=status.HTTP_201_CREATED
#                 )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class PledgeDetail(APIView):

#     def get_object(self, pk):
#         try:
#             pledge = Pledge.objects.get(pk=pk)
#             return pledge
#         except Pledge.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk):
#         pledge = self.get_object(pk)
#         serializer = PledgeSerializer(pledge)
#         return Response(serializer.data)
    







# TEST STUFF
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pledge
from .serializers import PledgeSerializer
from rest_framework import status

class PledgeList(APIView):
    def get(self, request):
        # Retrieve all pledges that are not deleted
        pledges = Pledge.objects.filter(is_deleted=False)
        
        # Serialize the pledges
        serializer = PledgeSerializer(pledges, many=True)
        
        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Ensure that the 'project' field is provided in the request data
        pledge_data = request.data
        project_id = pledge_data.get('project')
        if project_id is None:
            return Response(
                {'error': 'The "project" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            project = Project.objects.get(pk=project_id, is_open=True)
        except Project.DoesNotExist:
            return Response(
                {'error': 'The specified project does not exist or is not open.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create and save the new pledge without requiring a supporter
        serializer = PledgeSerializer(data=pledge_data)
        if serializer.is_valid():
            serializer.save(supporter=None, is_deleted=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)