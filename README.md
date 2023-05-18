<h1>PeoplePedia</h1>
<p>The backend-end for PeoplePedia, an AI powered search engine that summarizes and visualizes information for anyone who has data on the internet.</p>

<p align="left"> 
  <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> 
    <img src="https://www.vectorlogo.zone/logos/djangoproject/djangoproject-ar21.svg" alt="Django"  height="60"/> 
  </a> 
  <a href="https://www.microsoft.com/en-us/bing/apis/bing-web-search-api" target="_blank" rel="noreferrer"> 
    <img src="https://www.vectorlogo.zone/logos/bing/bing-ar21.svg" alt="Bing Web Search" height="60" /> 
  </a> 
  <a href="https://dashboard.heroku.com/apps" target="_blank" rel="noreferrer"> 
    <img src="https://www.vectorlogo.zone/logos/heroku/heroku-ar21.svg" alt="Herku" height="60"/> 
  </a> 
  <a href="https://openai.com/" target="_blank" rel="noreferrer">
    <img src="https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg" alt="Herku" height="50"/>
  </a> 
</p>

![image](https://user-images.githubusercontent.com/66019710/228403877-bea9568f-96d1-4897-b5e8-01dcece7a52e.png)
![image](https://user-images.githubusercontent.com/66019710/228404612-d4bacfc7-566a-476a-8619-5a019b86f508.png)

<h2>Explanation</h2>
<ol>
    <li>Recieves a JSON object {"name":"Elon Musk"} from the front-end</li>
    <li>Performs a Bing Web-Search on the name field and receives X summarized webpages</li>
    <li>Using prompt engineering, the back-end posts this data to the OpenAI text-davinci-003 model and receives a standardized JSON response (featured below)</li>
    <li>STRONGLY serializes this JSON response (check serializer.py)</li>
    <li>Returns this object to the front-end</li>
</ol>

<h2>Properties</h2>
<p>This JSON object is returned to the front-end.</p>
<ul>
  <li><strong>age:</strong> a string representing the age of the person</li>
  <li><strong>analysis:</strong> an array of JSON objects representing different types of analysis. Each JSON object in the analysis array contains the following keys:
    <ul>
      <li><strong>attribute:</strong> a string representing the type of analysis being performed</li>
      <li><strong>confidence:</strong> a string representing the level of confidence in the analysis (e.g. "HIGH", "MEDIUM", "LOW")</li>
      <li><strong>explanation:</strong> a string explaining the results of the analysis</li>
      <li><strong>score:</strong> a float representing the score or value associated with the analysis</li>
      <li><strong>url_list:</strong> an array of strings representing relevant URLs for the analysis</li>
    </ul>
  </li>
  <li><strong>conclusion:</strong> a string summarizing the person's background or profile</li>
  <li><strong>education:</strong> a JSON object representing the person's educational background. The education object contains the following keys:
    <ul>
      <li><strong>institution:</strong> a string representing the name of the educational institution attended</li>
      <li><strong>degree:</strong> a string representing the degree(s) earned</li>
      <li><strong>graduation_year:</strong> a string representing the year of graduation</li>
    </ul>
  </li>
  <li><strong>location:</strong> a string representing the person's current location</li>
  <li><strong>msc:</strong> an array of JSON objects representing the person's goals, interests, and skills. Each JSON object in the msc array contains the following keys:
    <ul>
      <li><strong>category:</strong> a string representing the category of the goal, interest, or skill</li>
      <li><strong>details:</strong> an array of strings representing specific details about the goal, interest, or skill</li>
    </ul>
  </li>
  <li><strong>name:</strong> a string representing the name of the person</li>
  <li><strong>occupation:</strong> a string representing the person's occupation or profession</li>
  <li><strong>photo:</strong> a string representing the URL of a photo of the person</li>
</ul>


<h2>Example Object</h2>
<pre>{
"age": "50",
"analysis": [
{
"attribute": "Political Alignment",
"confidence": "HIGH",
"explanation": "Elon Musk has not publicly expressed a political alignment.",
"score": 0,
"url_list": [
"https://twitter.com/elonmusk",
"https://www.cnn.com/2023/03/28/tech/elon-musk-verified-only-for-you-feed/index.html",
"https://www.britannica.com/biography/Elon-Musk",
"https://en.wikipedia.org/wiki/Elon_Musk"
]
},
{
"attribute": "Sentiment",
"confidence": "LOW",
"explanation": "Elon Musk is a well-respected entrepreneur, innovator and philanthropist.",
"score": 0.45,
"url_list": [
"https://twitter.com/elonmusk",
"https://www.cnn.com/2023/03/28/tech/elon-musk-verified-only-for-you-feed/index.html",
"https://www.britannica.com/biography/Elon-Musk",
"https://en.wikipedia.org/wiki/Elon_Musk"
]
}
],
"conclusion": "Elon Musk is an American entrepreneur responsible for co-founding the electronic-payment firm PayPal, forming SpaceX and being one of the first significant investors in, as well as chief executive officer of, the electric car manufacturer Tesla. In addition, he acquired Twitter in 2022.",
"education": {
"institution": "University of Pennsylvania",
"degree": "B.S. Economics & B.S. Physics",
"graduation_year": "1995"
},
"location": "Pretoria, South Africa & United States",
"msc": [
{
"category": "Goals",
"details": [
"Democratize space transportation",
"Sustainably reduce the cost of building and launching rockets",
"Construct a human colony on Mars"
]
},
{
"category": "Interests",
"details": [
"Innovative technology",
"Business and venture capital"
]
},
{
"category": "Skills",
"details": [
"Business acumen",
"Programming expertise",
"Advanced knowledge of electric engine mechanics"
]
}
],
"name": "Elon Musk",
"occupation": "Entrepreneur",
"photo": "https://tse4.mm.bing.net/th?id=OIP.ddIZudKNg4dgPdTUYy7UxAHaFQ&pid=Api"
}</pre>
