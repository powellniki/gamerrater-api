from raterapi.models import Game, Category
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class GameView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serialized = GameSerializer(game, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response({'message': 'The game you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        games = Game.objects.all()
        serialized = GameSerializer(games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


    def create(self, request):
        # extract fields from client request body
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        designer = request.data.get('designer', None)
        release_year = request.data.get('year', None)
        number_players = request.data.get('players', None)
        play_time = request.data.get('playTime', None)
        age_rec = request.data.get('ageRec', None)
        user=request.user

        if title is None or description is None or designer is None or release_year is None or number_players is None or play_time is None or age_rec is None:
            return Response({'message': 'You must provide all properties in your JSON'}, status=status.HTTP_400_BAD_REQUEST)

        #create an instance of needed model, set properties
        new_game = Game()
        new_game.title = title
        new_game.description = description
        new_game.designer = designer
        new_game.release_year = release_year
        new_game.number_players = number_players
        new_game.play_time = play_time
        new_game.age_rec = age_rec
        new_game.user = user
        new_game.save()

        # serialize the newly created game
        serialized_game = GameSerializer(new_game, many=False)

        #send data back in a response with 201 status code
        return Response(serialized_game.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        pass


    def destroy(self, request, pk):
        pass

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]

class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'release_year', 'number_players', 'play_time', 'age_rec', 'categories', )