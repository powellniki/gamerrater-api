from raterapi.models import Review, Game
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class ReviewView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            serialized = ReviewSerializer(review, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)

        except Review.DoesNotExist:
            return Response({'message': 'The review you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def list(self, request):
        reviews = Review.objects.all()
        serialized = ReviewSerializer(reviews, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):

        # extract fields from client request body
        game_id = request.data.get('game', None)
        game_instance = Game.objects.get(pk=game_id)
        user=request.user
        review = request.data.get('review', None)

        if game_id is None or review is None:
            return Response({'message': 'You must provide all properties in your JSON'}, status=status.HTTP_400_BAD_REQUEST)

        #create an instance of needed model, set properties
        new_review = Review()
        new_review.game = game_instance
        new_review.user = user
        new_review.review = review

        new_review.save()

        # serialize the newly created game
        serialized_review = ReviewSerializer(new_review, many=False)

        #send data back in a response with 201 status code
        return Response(serialized_review.data, status=status.HTTP_201_CREATED)
    
class GameReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('title',)

class ReviewSerializer(serializers.ModelSerializer):
    game = GameReviewSerializer(many=False)

    class Meta:
        model = Review
        fields = ('id', 'game', 'user', 'review',)