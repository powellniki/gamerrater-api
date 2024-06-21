from raterapi.models import Game, Category
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class GameView(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serialized = GameSerializer(game, many=False, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response({'message': 'The game you requested does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        games = Game.objects.all()
        serialized = GameSerializer(games, many=True, context={'request': request})
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


    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)

            # is the authenticated user allowed to edit the game?
            self.check_object_permissions(request, game)

            serializer = GameSerializer(data=request.data)
            if serializer.is_valid():
                game.title = serializer.validated_data['title']
                game.description = serializer.validated_data['description']
                game.designer = serializer.validated_data['designer']
                game.release_year = serializer.validated_data['release_year']
                game.number_players = serializer.validated_data['number_players']
                game.play_time = serializer.validated_data['play_time']
                game.age_rec = serializer.validated_data['age_rec']
                game.save()

                serializer = GameSerializer(game, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        pass

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]

class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    # Declare that an ad-hoc property should be included in JSON
    is_owner = serializers.SerializerMethodField()

    # Function containing instructions for ad-hoc property
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user

    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'release_year', 'number_players', 'play_time', 'age_rec', 'is_owner', 'categories', )