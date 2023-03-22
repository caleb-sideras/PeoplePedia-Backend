from rest_framework import serializers
from enum import Enum
from django.core.serializers.json import DjangoJSONEncoder

BANNED_WORDS = ['anal', 'anus', 'arse', 'ass', 'balls', 'ballsack', 'bastard', 'biatch', 'bitch', 'bloody', 'blow job', 'blowjob', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'crap', 'cunt', 'damn', 'dick', 'dildo', 'dyke', 'f u c k', 'fag', 'feck', 'felching', 'fellate', 'fellatio', 'flange', 'fuck', 'fudge packer', 'fudgepacker', 'God damn', 'Goddamn', 'hell', 'homo', 'jerk', 'jizz', 'knob end', 'knobend', 'labia', 'lmao', 'lmfao', 'muff', 'nigga', 'nigger', 'omg', 'penis', 'piss', 'poop', 'prick', 'pube', 'pussy', 'queer', 's hit', 'scrotum', 'sex', 'sh1t', 'shit', 'slut', 'smegma', 'spunk', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore', 'wtf']

def handle_nullable_field(field, value):
    if value is None or value.lower() == "N/A":
        if isinstance(field, serializers.ListField):
            return []
        elif isinstance(field, serializers.CharField):
            return ""
        elif isinstance(field, serializers.IntegerField):
            return 0
        elif isinstance(field, serializers.FloatField):
            return 0.0
        elif isinstance(field, serializers.BooleanField):
            return False
        else:
            return None
    else:
        return value

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=20)

    def validate_query(self, value):
        if len(value) > 25:
            raise serializers.ValidationError(
                "Query must be less than 25 characters.")

        words = value.split()
        for word in words:
            if word.lower() in BANNED_WORDS:
                raise serializers.ValidationError(
                    f"Query cannot contain '{word}'.")

        return value

class CustomEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ConfidenceEnum): # check if obj is an enum instance
            return obj.name # return the name of the enum value
        return super().default(obj) # otherwise use the default encoder

class ConfidenceEnum(Enum):
  HIGH = 1
  MEDIUM = 2
  LOW = 3

class ConfidenceField(serializers.Field):
  def to_representation(self, obj):
    return obj.name

  def to_internal_value(self, data):
    if isinstance(data, str):
      try:
        return ConfidenceEnum[str.upper(data)]
      except KeyError:
         return ConfidenceEnum.LOW
        # raise serializers.ValidationError(
        #   f"Invalid value for confidence: {data}. Expected one of: {', '.join([e.name for e in ConfidenceEnum])}"
        # )
    elif isinstance(data, int):
      try:
        return ConfidenceEnum(data)
      except ValueError:
         return ConfidenceEnum.LOW
        # raise serializers.ValidationError(
        #   f"Invalid value for confidence: {data}. Expected one of: {', '.join([str(e.value) for e in ConfidenceEnum])}"
        # )
    else:
      raise serializers.ValidationError(
        f"Invalid type for confidence: {type(data)}. Expected str or int.")

class EducationSerializer(serializers.Serializer):
    institution = serializers.CharField(allow_blank=True, allow_null=True, default="")
    degree = serializers.CharField(allow_blank=True, allow_null=True, default="")
    graduation_year = serializers.CharField(allow_blank=True, allow_null=True, default="")
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in self.fields:
            ret[field] = handle_nullable_field(self.fields[field], ret[field])
        return ret

class AnalysisSerializer(serializers.Serializer):
    attribute = serializers.CharField(allow_blank=True, allow_null=True, default="")
    score = serializers.FloatField(min_value=-1.0, max_value=1.0, default=0.0, allow_null=True) # add min and max values
    explanation = serializers.CharField(allow_blank=True, allow_null=True, default="")
    url_list = serializers.ListField(child=serializers.CharField(), allow_empty=True, default=[])
    confidence = ConfidenceField() # change choices to tuples

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in self.fields:
            ret[field] = handle_nullable_field(self.fields[field], ret[field])
        return ret

class SkillSerializer(serializers.Serializer):
    category = serializers.CharField(allow_blank=True, allow_null=True, default="")
    details = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in self.fields:
            ret[field] = handle_nullable_field(self.fields[field], ret[field])
        return ret

class MainSerializer(serializers.Serializer):
    photo = serializers.CharField(allow_blank=True, allow_null=True, default="") # add photo field
    name = serializers.CharField(allow_blank=True, allow_null=True, default="")
    conclusion = serializers.CharField(allow_blank=True, allow_null=True, default="") # add conclusion field
    age = serializers.CharField (allow_blank=True, allow_null=True, default="")
    location = serializers.CharField(allow_blank=True, allow_null=True, default="") # add location field
    occupation = serializers.CharField(allow_blank=True, allow_null=True, default="")
    education = EducationSerializer()
    analysis = AnalysisSerializer(many=True, allow_null=True, allow_empty=True)
    msc = SkillSerializer(many=True, allow_null=True, allow_empty=True)