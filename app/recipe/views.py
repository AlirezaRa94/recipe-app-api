from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttrViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """ Base view set for user owned recipe attributes """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new object for the current authenticated user only """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """ Manage tags in the database """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredients in the database """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    """ Manage recipes in the database """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retrieve the recipes for the authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ Return appropriate serializer class """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return serializers.RecipeSerializer

    def perform_create(self, serializer):
        """ Create a new recipe for the authenticated user only """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to a recipe """
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
