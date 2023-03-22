from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from quickstart.serializers import QuerySerializer, MainSerializer, CustomEncoder
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import throttle_classes
from django.conf import settings
import requests
import openai
import json
import json5

# KEYS
secret_key = settings.SECRET_KEY
BING_SEARCH_SUBSCRIPTION_KEY = settings.BING_SEARCH_SUBSCRIPTION_KEY
BING_SEARCH_SUBSCRIPTION_KEY2 = settings.BING_SEARCH_SUBSCRIPTION_KEY2
OPENAI_API_KEY = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION
openai.api_key = OPENAI_API_KEY
openai.Model.list()

# ENDPOINTS
BING_SEARCH_ENDPOINT = settings.BING_SEARCH_ENDPOINT
BING_IMAGE_SEARCH_ENDPOINT = settings.BING_IMAGE_SEARCH_ENDPOINT
OPENAI_DAVINCI_ENDPOINT = settings.OPENAI_DAVINCI_ENDPOINT
OPENAI_TURBO_ENDPOINT = settings.OPENAI_TURBO_ENDPOINT

# CONST VARIABLES
modelDavinci = "text-davinci-003"
modelTurbo = "gpt-3.5-turbo"

initStr = 'using the following data '
mStr1 = ' generate an overall analysis using the follwing schema, with '
analysis = ['Political Alignment', 'Sentiment', 'Education']
mStr2 = ' for analysis and '
msc = ['Goals', 'Interests', 'Skills']
mStr3 = ' for msc ' 
endStr = ' RETURN A VALID JSON'

midStr = mStr1 + ",".join(analysis) + mStr2 + ",".join(msc) + mStr3

# SCHEMAS
schemaV1 = """{"name":String,"conclusion":String,"age":String,"location":String,"occupation":String,"education":{"institution":String,"degree":String,"graduation_year":String},"analysis":[{"attribute":String,"score":float{-1-1},"explanation":String,"url_list":[String],"confidence":Enum{"HIGH"=1,"MEDIUM"=2,"LOW"=3}}],"msc":[{"category":String,"details":[String]}]}"""

# API HEADERS
bingHeader = {"Ocp-Apim-Subscription-Key": BING_SEARCH_SUBSCRIPTION_KEY}
openaiHeader = {"Content-Type": "application/json",
                "Authorization": f"Bearer {openai.api_key}"}

# class QueryRateThrottle(SimpleRateThrottle):
#     rate = "1/30s"

# @throttle_classes([QueryRateThrottle])


def send_request(endpoint, headers, params, rtype, timeout=30):
    try:
        if rtype:
            response = requests.get(endpoint, headers=headers, params=params, timeout=timeout)
        else:
            response = requests.post(endpoint, headers=headers, json=params, timeout=timeout)

        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
        return "The AI did an oopsie, try again"
    except requests.exceptions.Timeout as timeout_error:
        print(f"Request timed out: {timeout_error}") 
        return "The AI did an oopsie, try again"
    except requests.exceptions.RequestException as request_error:
        print(f"An error occurred: {request_error}")
        return "The AI did an oopsie, try again"

@throttle_classes([UserRateThrottle, AnonRateThrottle])
class QueryView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):

        
        serializer = QuerySerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({"Please do not use profanity"}, status=400)
        
        query = serializer.validated_data["query"]

        # bing image api call
        imageParams = {"q": query, "mkt": "en-US", "count" : 3}
        print("Image API")
        response = send_request(BING_IMAGE_SEARCH_ENDPOINT, bingHeader, imageParams, True, timeout=30)
        if type(response) == str:
            return Response(response, status=400)
        imgResults = response.json()

        # sanitizing
        imgData = [{'name': v.get('name'), 'url': v.get('thumbnailUrl')} for v in imgResults.get('value', [])]
        url = next((obj['url'] for obj in imgData if any(n in obj['name'] for n in query.split())), "")
        print(url)

        # bing api call
        bingParams = {"q": query, "mkt": "en-US", "count" : 5}
        print("Bing API")
        response = send_request(BING_SEARCH_ENDPOINT, bingHeader, bingParams, True, timeout=30)
        if type(response) == str:
            return Response(response, status=400)
        searchResults = response.json()

        # sanitizing
        bingData = [{'name': v.get('name'), 'url': v.get('url'), 'snippet': v.get(
            'snippet')} for v in searchResults.get('webPages', {}).get('value', [])]
        # print(bingData)

        # openai api call
        jsonContent = initStr + str(bingData) + midStr + schemaV1 + endStr
        # print(jsonContent)
        openaiParams = {
            "model": modelDavinci,
            "prompt": jsonContent,
            "max_tokens": 1200,
            # max_tokens (2064) - prompt_tokens - margin of 10%
        }
        # openaiParams = {
        #     "model": modelTurbo, 
        #     "messages": [
        #     {"role": "system", "content": "RETURN A VALID JSON"},
        #     {"role": "user", "content": jsonContent}
        #     ],
        # }
        print("OPENAI API")
        response = send_request(OPENAI_DAVINCI_ENDPOINT, openaiHeader, openaiParams, False, timeout=60)
        if type(response) == str:
            return Response(response, status=400)
        searchResults = response.json()
        
        response.raise_for_status()
        gptSearchResults = response.json()
        print(gptSearchResults['usage'])


        if not gptSearchResults.get('choices', False):
            print('choices field not in gpt reponse')
            return Response({"GTP-3 did an oopsie"}, status=400)
        if len(gptSearchResults['choices']) <= 0 and not gptSearchResults['choices'][0]['text']:
            print('choiceslen and/or text field not in gpt reponse')
            return Response({"GTP-3 did an oopsie"}, status=400)
        
        textJson = gptSearchResults['choices'][0]['text']
        if not isinstance(textJson, dict):
            try:
                start_index = textJson.find('{')
                textJson = json.loads(textJson[start_index:])
            except json.JSONDecodeError as e:
                try:
                    # decoder = json.JSONDecoder(strict=False)
                    # textJson = decoder.decode(textJson[start_index:])
                    textJson = json5.loads(textJson[start_index:])
                    print("USED JSON5")
                except (json.JSONDecodeError, ValueError) as e:
                    print(textJson[start_index:])
                    print(type(textJson))
                    print(f"loads and JSONDecoder failed, Invalid JSON: {e}")
                    return Response({"GTP-3 did an oopsie"}, status=400)

        textJson['photo'] = url
        gptSerializer = MainSerializer(data=textJson)

        if not gptSerializer.is_valid():
            print(gptSerializer.errors)
            return Response({"GTP-3 did an oopsie"}, status=400)
        json_data = json.dumps(gptSerializer.validated_data, cls=CustomEncoder)
        # print(json_data)

        return Response({"message": "Query accepted.", "query": json.loads(json_data)}, status=200)