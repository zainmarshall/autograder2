from rest_framework import serializers

class StandingsRowSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    solved = serializers.IntegerField()
    penalty = serializers.IntegerField()
    rank = serializers.IntegerField()
    problems = serializers.ListField(child=serializers.IntegerField())

class StandingsSerializer(serializers.Serializer):
    title = serializers.CharField()
    pnum = serializers.IntegerField()
    load = StandingsRowSerializer(many=True)