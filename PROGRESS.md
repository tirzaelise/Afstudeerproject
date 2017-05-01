### Thursday 13/04/2017

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

### Wednesday 19/04/2017

Interesting papers:

1.  Summary of  Symbol emergence in robotics for long-term human-robotcollaboration [Taniguchi,  2016]:   Symbol  emergence       in  robotics  is  anemerging research field that attempts to solve interdisciplinary problems related to ‘symbols’ using     the constructive approach with robotic and machine learning technologies.  It is important that a robot has an adaptive       cognitive capability to become a symbol emergence system (a symbol system  that  is  maintained  by  a  complex  system       that  involves  people  who perform semitiotic communications). 
    Gives several computational models, which provide a model to understand cognitive phenomena related to symbol emergence.     Such as multimodal categorisation,  which  is  used  to  reproduce  the  process  of  forming  categories and concepts       based on experience, and spatial concept formation, which organises the robot’s memory to integrate information about         places, names, objects, and tasks related to  the place.  Driving behaviour  datawas used to perform double articulation     analysis (a stream of speech can be  divided  into  meaningful  signs,  which  can  be  further  subdivided  into             meaningless elements), which showed that a driving word and a driving letter represent the segments in driving behavior       data, corresponding to a  word  and  phoneme  in  speech  signals.   Also  gives  several  methods  for language             acquisition.

    Link to own project:  Multimodal categorisation is a method to form categories and concepts based on experience, which       could be used to create and update the knowledge base of the robot.  Spatial concept formation organises the robot’s         memory to integrate information about places, names, objects, and tasks related to a place, which could be used to create     the link between a customer, their drink order and their position.
    
### Thursday 20/04/2017

Meeting points:

- Literature research: What have others done, what will I include of this and what will I not include
- Research: What is my problem and how will I approach this
- Hourglass context: AI -> robotics -> RoboCup@Home -> social (partial solution)
- RoboCup@Home publications clustered by theme: https://robocup.rwth-aachen.de/athomewiki/index.php/Publications#Human-Robot_Interaction</br></br>

- Find classical works (state of the art) of dialogue of different cultures (Japanese, English)
- Fill a database with facts about cocktails/drinks from the internet and flag which ones the barman can make
- Which formats of dialogue can be used at the bar</br></br>

- Free dialogue in games
- Research question flexibility: Can I have a flexible conversation with a bar robot? -> Prove that you can
- Research question with human testing</br></br>

Interesting papers:

2.  Summary of Integrated learning of dialog strategies and semantic parsing [Padmakumar et al., 2017]:  Presents an approach     to integrate the learning of a dialog strategy using reinforcement learning and a semantic parser for robust natural         language understanding, using only natural dialog interaction for supervision.  Reinforcement learning algorithms assume     that  the  dialog agent  is  operating  in  a  stationary  environment, but this assumption is violated when the parser       is updated between conversations.  This effect can be mitigated by breaking the allowed budget of training dialogs into       batches.  As the next training batch gets collected using  the  updated  parser,  the  policy  can  be  updated  using       this  experience to adapt better to it.  The system asks for an initial command, after which  it  asks  for                   clarification  until  it understands  the  command  correctly.   Semantic  parsing  is  performed  using  probabilistic       CKY-parsing with a Combinatory Categorial Grammar and meanings associated with lexical entries.

    Link to own project: A similar method could be used to ask clarifying questions to the barman and to be able to               understand his responses.
    
3.  Summary of Artificial Cognition for Social Human-Robot Interaction: An Implementation [Lemaignan  et  al.,  2016]:           Characterises  the  challenges  of human-robot interaction in artificial intelligence and exhibits a set of key               decisional issues that need to be addressed for a cognitive robot to successfully share space and tasks with a human.         Natural language grounding is done using the Google speech recognition API for speech-to-text, after which the text is       parsed into a grammatical structure (POS tagging) using a custom heuristics-based parser.  The resulting atoms are           resolved with the help of the knowledge base to ground concepts like objects. 

    Link to  own  project:  This  article  shows  an  interesting  way  to  perform natural language grounding, which I could     also use for my thesis, since I will be working with a knowledge base as well.
    
4.  Summary of Grounding the Interaction: Anchoring Situated Discourse in Everyday Human-Robot Interaction [Lemaignan et al.,     2012]:  This paper explains exactly how the natural language grounding of the previous paper is done. Three categories of     sentences are produced:  statements,  desires and questions that can be answered from the declarative knowledge present       in the robot knowledge base.  The grounding process consists of extracting either the informational content of the           sentence to produce statements or its intentional content to collect orders and questions. The module processes human         input in natural language, grounds the concepts in the robot’s knowledge and eventually translates the discourse in a set     of queries or declarative OWL/RDF statements.

    Link to own project: The grounding process could be used to find out what the barman is talking about.

### Friday 21/04/2017

Interesting papers:

5.  Summary of Development  of  a  tour–guide  robot  using dialogue models and a cognitive architecture [Avilés et al.,         2010]: Shows how a tour guide robot is able to navigate around its environment, visually identify informational posters       and explain sections of the poster that users request via pointing gestures. The task that the robot performs is             determined by a dialogue model, which defines conversational situations, expectations and robot actions. Speech               recognition is based on general acoustic-phonetic models. When a sentence is recognised, the speech is interpreted by         comparing the sentence with a set of equivalent regular expressions defined for each expectation. If no match is found,       the user is requested for another attempt.

    Link to own project:  Shows that earlier speech interpretation work was done  using  regular  expressions. This  article     also  shows  a  really  clear way to create a dialogue  model, which I could use as inspiration to create my own.
    
6.  Summary of Designing and evaluating an adaptive spoken dialogue system [Litman and Pan, 2002]: Presents the design and       evaluation of an adaptive spoken dialogue system (TOOT), which  retrieves online train schedules. It constructs a user       model whether the user is having speech recognition problems as the dialogue progresses, based on rules learned from a       set of training dialogues. In which case it automatically adapts the dialogue strategies.

    Link to own project: This article shows a clear algorithm that determines when to change the dialogue strategy if there       have been speech recognition problems.
    
I also read a lot of papers about natural language generation and creating dialogues, but I couldn't find anything that was interesting for my project. 

## Monday 24/04/2017

I spent the entire day working on my research proposal and making a planning until the final deadline.

## Tuesday 25/04/2017

I spent the entire working on my research proposal and my presentation.

## Wednesday 26/04/2017

I held my research proposal presentation in the morning and then I spent the entire day working on my research proposal document again.

## Monday 01/05/2017

Started working on the drinks database. The ADDb API structure of a drink is as contains the following properties that are interesting for my project: name, descriptionPlain, color, skill, isAlcoholic, isCarbonated, isHot, ingredients, tastes, occasions, tools, actions. I tried to work with AsyncTasks since I have done this before, but then I realised that this is only available for Java coding for Android. Therefore, I chose to work with Python instead. I implemented code to scrape a web page and retrieve all the interesting properties to put create a Drink object.
