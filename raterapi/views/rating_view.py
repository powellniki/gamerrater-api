from raterapi.models import Rating, Game
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class RatingView(ViewSet):

    def retrieve(self, request, pk=None):
        pass

    def list(self, request):
        pass

    def create(self, request):
        # extract fields from client request body
        game_id = request.data.get('game', None)
        game_instance = Game.objects.get(pk=game_id)
        user=request.user
        rating = request.data.get('rating', None)

        if game_id is None or rating is None:
            return Response({'message': 'You must provide all properties in your JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
        #create an instance of needed model, set properties
        new_rating = Rating()
        new_rating.game = game_instance
        new_rating.user = user
        new_rating.rating = rating

        new_rating.save()

        # serialize the newly created game
        serialized_rating = RatingSerializer(new_rating, many=False)

        #send data back in a response with 201 status code
        return Response(serialized_rating.data, status=status.HTTP_201_CREATED)


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'game', 'rating', 'user')