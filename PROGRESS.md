## Thursday 13/04/2017

<b>Assignment</b> </br>

- Placing the orders: The robot has to navigate to the Bar, a designated location in another room where drinks are served. The 
robot must repeat each order to the Barman, clearly stating: </br></br>
(a) The person’s name, </br>
(b) The person’s chosen drink, </br>
(c) A description of unique characteristics of that person that allow the Barman to find them (e.g. gender, hair colour, 
how is dressed, etc). </br></br>
While the robot places the orders, the people in the “party room” may change their places within the party room 
(on request of the referees).</br></br>
- Missing beverage: One of the ordered drinks is not available, therefore, missing from the bar. The robot should realize 
this inconvenience and tell the Barman, providing a list of 3 alternatives considering the other drinks it needs to deliver. If
the robot can’t detect which drink is missing, the Barman will clearly state which of the beverages is not available and 
provide a list of 3 alternatives.

<b>General idea</b> </br>
1. Create a model of what the bar man knows and doesn't know
2. Make conversation in order to find out if this is correct
3. Model: drinks -> Use web to find out what cocktails are available (ingredients, procedures, connection with preferences of customers)

Find literature that explains how to build a conversation and a narrative, as well as how to connect them to a knowledge system. 

## Wednesday 19/04/2017

Interesting papers:

1.  Summary of  <a href="http://ac.els-cdn.com/S2405896316320663/1-s2.0-S2405896316320663-main.pdf?_tid=f1d621fe-252c-11e7-9901-00000aab0f02&acdnat=1492626242_e12af5ab44edcf338cd7fd3a4635f492">Symbol emergence in robotics for long-term human-robot collaboration</a> [Taniguchi,  2016]:   Symbol  emergence in  robotics is  anemerging research field that attempts to solve interdisciplinary problems related to ‘symbols’ using the constructive approach with robotic and machine learning technologies.  It is important that a robot has an adaptive cognitive capability to become a symbol emergence system (a symbol system  that  is  maintained by a complex system that involves people who perform semitiotic communications). Gives several computational models, which provide a model to understand cognitive phenomena related to symbol emergence. Such as multimodal categorisation, which is used to reproduce the process of forming categories and concepts based on experience, and spatial concept formation, which organises the robot’s memory to integrate information about places, names, objects, and tasks related to the place. Driving behaviour data was used to perform double articulation analysis (a stream of speech can be divided into meaningful signs, which can be further subdivided into meaningless elements), which showed that a driving word and a driving letter represent the segments in driving behavior data, corresponding to a  word  and  phoneme  in  speech  signals. Also gives several methods for language acquisition.

    Link to own project: Multimodal categorisation is a method to form categories and concepts based on experience, which       could be used to create and update the knowledge base of the robot.  Spatial concept formation organises the robot’s         memory to integrate information about places, names, objects, and tasks related to a place, which could be used to create the link between a customer, their drink order and their position.
    
## Thursday 20/04/2017

Meeting points:

- Literature research: What have others done, what will I include of this and what will I not include
- Research: What is my problem and how will I approach this
- Hourglass context: AI -> robotics -> RoboCup@Home -> social (partial solution)
- <a href="https://robocup.rwth-aachen.de/athomewiki/index.php/Publications#Human-Robot_Interaction">RoboCup@Home publications clustered by theme</a></br></br>

- Find classical works (state of the art) of dialogue of different cultures (Japanese, English)
- Fill a database with facts about cocktails/drinks from the internet and flag which ones the barman can make
- Which formats of dialogue can be used at the bar</br></br>

- Free dialogue in games
- Research question flexibility: Can I have a flexible conversation with a bar robot? -> Prove that you can
- Research question with human testing</br></br>

Interesting papers:

2. Summary of <a href="http://www.cs.utexas.edu/users/ml/papers/padmakumar.eacl17.pdf">Integrated learning of dialog strategies and semantic parsing</a> [Padmakumar et al., 2017]:  Presents an approach to integrate the learning of a dialog strategy using reinforcement learning and a semantic parser for robust natural language understanding, using only natural dialog interaction for supervision.  Reinforcement learning algorithms assume that the dialog agent is operating in a stationary  environment, but this assumption is violated when the parser is updated between conversations. This effect can be mitigated by breaking the allowed budget of training dialogs into batches. As the next training batch gets collected using the updated parser, the policy can be updated using this  experience to adapt better to it.  The system asks for an initial command, after which it asks for clarification until it understands the command correctly. Semantic parsing is performed using probabilistic CKY-parsing with a Combinatory Categorial Grammar and meanings associated with lexical entries.

    Link to own project: A similar method could be used to ask clarifying questions to the barman and to be able to understand his responses.
    
3. Summary of <a href="https://www.researchgate.net/profile/Severin_Lemaignan/publication/305208728_Artificial_Cognition_for_Social_Human-Robot_Interaction_An_Implementation/links/5784b2b408ae3f355b4bae7f.pdf">Artificial Cognition for Social Human-Robot Interaction: An Implementation</a> [Lemaignan  et  al.,  2016]: Characterises the challenges of human-robot interaction in artificial intelligence and exhibits a set of key decisional issues that need to be addressed for a cognitive robot to successfully share space and tasks with a human. Natural language grounding is done using the Google speech recognition API for speech-to-text, after which the text is parsed into a grammatical structure (POS tagging) using a custom heuristics-based parser.  The resulting atoms are resolved with the help of the knowledge base to ground concepts like objects. 

    Link to own  project: This article shows an interesting way to perform natural language grounding, which I could     also use for my thesis, since I will be working with a knowledge base as well.
    
4. Summary of <a href="https://hal.archives-ouvertes.fr/hal-00664546/document">Grounding the Interaction: Anchoring Situated Discourse in Everyday Human-Robot Interaction</a> [Lemaignan et al., 2012]: This paper explains exactly how the natural language grounding of the previous paper is done. Three categories of sentences are produced: statements, desires and questions that can be answered from the declarative knowledge present in the robot knowledge base. The grounding process consists of extracting either the informational content of the sentence to produce statements or its intentional content to collect orders and questions. The module processes human input in natural language, grounds the concepts in the robot's knowledge and eventually translates the discourse in a set of queries or declarative OWL/RDF statements.

    Link to own project: The grounding process could be used to find out what the barman is talking about.

## Friday 21/04/2017

Interesting papers:

5. Summary of <a href="http://calebrascon.info/pubre/IBERAMIA2010.Aviles2010.Article.pdf">Development of a tour–guide robot using dialogue models and a cognitive architecture</a> [Avilés et al., 2010]: Shows how a tour guide robot is able to navigate around its environment, visually identify informational posters and explain sections of the poster that users request via pointing gestures. The task that the robot performs is determined by a dialogue model, which defines conversational situations, expectations and robot actions. Speech recognition is based on general acoustic-phonetic models. When a sentence is recognised, the speech is interpreted by comparing the sentence with a set of equivalent regular expressions defined for each expectation. If no match is found, the user is requested for another attempt.

    Link to own project: Shows that earlier speech interpretation work was done using regular expressions. This article     also shows a really clear way to create a dialogue  model, which I could use as inspiration to create my own.
    
6. Summary of <a href="https://www.researchgate.net/profile/Diane_Litman/publication/220116357_Designing_and_Evaluating_an_Adaptive_Spoken_Dialogue_System/links/551441330cf2eda0df308ed0.pdf">Designing and evaluating an adaptive spoken dialogue system</a> [Litman and Pan, 2002]: Presents the design and evaluation of an adaptive spoken dialogue system (TOOT), which  retrieves online train schedules. It constructs a user model whether the user is having speech recognition problems as the dialogue progresses, based on rules learned from a set of training dialogues. In which case it automatically adapts the dialogue strategies.

    Link to own project: This article shows a clear algorithm that determines when to change the dialogue strategy if there have been speech recognition problems.
    
I also read a lot of papers about natural language generation and creating dialogues, but I couldn't find anything that was interesting for my project. 

## Monday 24/04/2017

I spent the entire day working on my research proposal and making a planning until the final deadline.

## Tuesday 25/04/2017

I spent the entire working on my research proposal and my presentation.

## Wednesday 26/04/2017

I held my research proposal presentation in the morning and then I spent the entire day working on my research proposal document again.

## Monday 01/05/2017

Started working on the drinks database. The ADDb API structure of a drink is as contains the following properties that are interesting for my project: name, descriptionPlain, color, skill, isAlcoholic, isCarbonated, isHot, ingredients, tastes, occasions, tools, actions. I tried to work with AsyncTasks since I have done this before, but then I realised that this is only available for Java coding for Android. Therefore, I chose to work with Python instead. I implemented code to scrape a web page and retrieve all the interesting properties to put create a Drink object. I also automated the process to retrieve all of the drinks that are in the ADDb (3637 drinks). I have to come up with a good way to save all this data.

## Tuesday 02/05/2017

I implemented code to save the database to a Pickle file. The data is saved in a Dictionary using the following format: {drink name: drink object}, which holds name, description, color, skill, is_alcoholic, is_carbonated, is_hot, ingredients, tastes, occasions, tools, actions. Also started working on the outline of my thesis.

## Wednesday 03/05/2017

Read a lot of articles about natural language understanding and installed <a href="http://www.nltk.org/">NLTK</a> and <a href="https://github.com/biplab-iitb/practNLPTools">practNLPTools</a>. The following articles might be interesting: https://pdfs.semanticscholar.org/ebe9/78c21cbc2a9e738b9fc9d257bbab2e093177.pdf?_ga=2.136246065.1014586811.1493814151-298941096.1493655434 and https://pdfs.semanticscholar.org/82c9/f475651e49c7eb8e98609fbdc4d8cc7c432a.pdf?_ga=2.183449966.919437324.1493810378-298941096.1493655434

practNLPTools can do semantic role labeling, syntactic parsing, part of speech tagging, named entity recognition, dependency parsing, shallow chunking. For my thesis, I am interested in semantic role labeling, part of speech tagging, named entity recognition and shallow chunking.

Conversation with Frank Nack:
- Starting point: What drinks from the menu can the barman make? 
- How important is a certain ingredient for a drink? Maybe there aren't any lemons, but the drink can also be prepared without a lemon.
- How does the robot communicate to the customer that there aren't any lemons available?
- Use 'tastes' and main ingredient to search for replacement drinks: "Would you like this drink instead of your ordered drink?"
- The dialogue model should represent that the robot takes on two different roles: asking questions and giving explanations
- How is a question built? -> Short and clear, a model that expects an answer
- How is an answer/explanation to a question built? -> A short list of ranked alternatives
- "This replacement comes closest to your ordered drink in taste"
- Be friendly to the customer but clear and short to the barman
- Use a set of templates for questions -> Elizabeth Andre (shopping assistants)
- Generate the question from the answer (flexible, but grammatical difficulties)
- Pattern matching 
- Description of the ingredients: "We use this type of ingredient in this drink, which is a bit more bitter than the other type."
- Write communication scenarios
- Generate questions based on what the customer wants
- Use a description cloud to ask the barman questions
- How should you ask a question such that you can use the template?

## Thursday 04/05/2017

I implemented code to convert a sentence into a logical form, for which I use the sentence's main verb, subject, object and (optional) negation. The sentence 'We do not have any ice' turns into have(not, we, ice). This is done using the practNLPTools semantic role labeling function. The logical translation is still very basic and will need to be improved. In order to make sure 'any' is not translated into the logical form, I assumed that the ending of a noun phrase is always the main noun.

## Tuesday 09/05/2017

I spent today improving the code I wrote to convert a natural sentence into its logical form. I did this using the dependency parse of practNLPTools. I am also starting to consider the fact that this might not be the best way to understand natural language and that machine learning would be a better option. But I need a data set if I want to do machine learning so I am looking into that right now. I also approached a language expert via e-mail and hope that they will reply and can help me. 

All the articles I read today did natural language understanding the same way. They had a Kinect microphone and used the Microsoft Kinect API for Windows, which produces a list of recognition hypotheses, an estimated confidence score and an estimate of the sound source angle and the angle confidence. The hypotheses are parsed to extract the syntactic and semantic information using a grammar implemented in OpenCCG.

Articles: <a href="http://www6.in.tum.de/Main/Publications/giuliani-etal-icmi2013.pdf">Comparing Task-Based and Socially Intelligent Behaviour in a Robot Bartender</a>, <a href="https://pdfs.semanticscholar.org/0f56/e1e51d6ede6ccd0574c8de00c61dbeec7ee2.pdf">Planning for Social Interaction in a Robot Bartender Domain</a>, <a href="http://www.dcs.gla.ac.uk/~mefoster/papers/foster-etal-hri2014.pdf">Towards Action Selection Under Uncertainty for a Socially Aware Robot Bartender</a>, <a href="https://pdfs.semanticscholar.org/aa26/04ea9212d13077002af83472476b59190553.pdf">How Can I Help You? Comparing Engagement Classification Strategies for a Robot Bartender</a>

## Wednesday 10/05/2017

Natural Language Understanding in <a href="http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7745086">
ERICA: The ERATO Intelligent Conversational Android</a>: The dialogue module compares received speech recognition results against a list of keywords. The utterance content and transition rules were scripted by hand. 

I noticed that a lot of state-of-the-art technologies used rule-based natural language understanding and natural language generation. Therefore, I decided to keep working in a rule-based manner. I wanted to combine rule-based NLP and machine learning, but I don't think I will have enough time to do this. Especially since I would also have to find a data set.

I rewrote a lot of code to understand natural language. Parsing is now done using StanfordDependencyParser, because this picked up on negations a lot better and it was a lot easier to work with than pracTNLPTools. I also started working on using NLTK's WordNet to find synonyms of verbs and nouns so that the robot can understand what is being said in a sentence.

Things that need to be done: Check whether a sentence is a question, this would change the dialogue path that has to be taken. Create a list of key words that holds most of the information about drinks that is in the database so that they can be checked for the NLU module.

## Thursday 11/05/2017

I wrote code to get all synonyms of a word using <a href="https://pypi.python.org/pypi/PyDictionary/1.3.4">PyDictionary</a>. I was going to use this to get all synonyms of the words in a natural sentence and check these against a list of key words. However, this is quite slow. Therefore, I am now going to generate the synonyms of all the words in the list of key words instead and hope this is faster to use. I wrote code to generate the key words, which was done using the drinks database. The key words are: the names of the drinks, the names of the drinks split on spaces, the descriptions of how to make the drinks split on spaces, the color of the drinks, the required skill level to make the drinks, the ingredients of the drinks, the occassions on which the drinks can be drunk, the tools required to make the drinks, and the actions required to make the drinks. I tried to run the code at night, unfortunately, but there was a bug.

Meeting points:
- Generate synonyms of key words instead of the words in a natural sentence
- Glue AI for a conversation model (Java)
- Story chat for story lines of stories and TV shows
- Use an evaluation form that people can fill in after testing the program: How natural was the conversation?
- Create a training and a test data set
- Evaluation: What's important is how the program came to the conclusion of what drinks were missing
- Evaluate how natural and robust the conversation was
- Thesis: What is necessary knowledge in order to understand the literature. What would you have wanted to know about natural dialogue before you started working?

## Friday 12/05/2017

I looked into using the Cheers script as a data set. One of the scripts I found was not annotated with a name so I would not be able to determine who is speaking without labeling this manually. Another script I found was annotated with a name, but in a scanned PDF format so I cannot parse this automatically. I also spent a lot of time looking at other data sources online, but I wasn't able to find anything.

I debugged the code to create the key words (24241 words). There is done a check to see if the words in a natural sentence occur in the key words. If they don't, then a string is generated that indicates what functions in the sentence were not understood. 

## Monday 15/05/2017

I worked on updating the knowledge base of ordered drinks once you receive information from a sentence. I am currently trying to do this with Wordnet's hypernyms, but it does not work well yet. I also rewrote my database code and it is now a Dictionary that holds: {drink name: list of drink properties}.

## Tuesday 16/05/2017

I finished writing the code to find the common hypernym between a word and a drink property (e.g. color, action, ingredient). I also wrote code to ask for confirmation once a sentence has been understood or misunderstood.

## Wednesday 17/05/2017

The synsets that are generated for a word and a drink property are now constrained by the desired POS tag. This makes sure that an action is found when a verb is fed into the program instead of a noun. Furthermore, whether a verb or a noun is used is no decided based on whether there is an object in the sentence or not, but on whether the verb expresses possession: e.g. have, possess, own, have got, hold. The most relevant drink property for a word is found using Wu-Palmer similarity instead of the shortest path distance.

## Thursday 18/05/2017

I spent a lot of time trying to get NAOqi working on my laptop, which I was able to fix by setting LD Library Path to the C++ NAOqi folder. But because of this, it was no longer possible to connect to a NAO robot. I wanted to test if it would be possible to use the ALSpeechRecognition API for the speech recognition of a sentence, but both my Python code and Choregraphe gave the error that ALSpeechRecognition could not be found. I'm not sure how to fix this yet.

Meeting points:
- It's better to get one component working well than each component working only half well
- SMACH (Ros)

## Friday 19/05/2017

I spent the day working on my literature review assignment for Academic English.

## Monday 22/05/2017

I managed to get ALSpeechRecognition working on my laptop and the Nao, but the downside of this speech recognition is that you have to indicate a time that the robot listens for. I found an Google Speech Recognition API for a Nao on Github, but this does not work with the Nao's microphone, it uses the microphone in your laptop. I am now looking into using Watson.

Great paper on speech recognition and how to use the microphones for NAOqi: <a href="https://arxiv.org/pdf/1704.04797.pdf">Setting Up Pepper For Autonomous Navigation And Personalized Interaction With Users</a>
