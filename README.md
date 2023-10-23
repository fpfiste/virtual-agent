# Master Thesis: Prototyping of a Digital Assistant for Helpdesk Services

This repository contains the prototype of a Digital Assistant which can be used in Enterprise Service Management. This code was the result of my Master Thesis.

## Research Objectives
The primary purpose of the thesis was to study the potential use of digital assistants in Enterprise Service Management (ESM). The overall research objective was to define what a digital assistant should look like and how it should be implemented. Therefore, the high-level requirements were determined, and a basic prototype was developed, implemented, and tested. 

## Methodology
The research documented in this thesis followed the agile development approach. Initially, the literature was reviewed, and the stakeholders were identified. Afterward, the requirements were defined, the prototype was planned, implemented, and tested iteratively. Interviews with representatives from the stakeholders were conducted. The prototype was then designed and implemented using a vertical prototyping approach. Eventually, the basic functionality was tested by performing unit- and integration tests.

## Results
A variety of functional and non-functional requirements could be identified. The following list gives an overview of these requirements:

* Task-orientation
* Skill variety
* User guidance
* Multilingualism
* System Evaluation
* Written interaction
* Personalization
* Accuracy
* Security
* Accessibility

The prototype’s architecture follows the generic architecture of a task-oriented dialog system, which was enhanced with the necessary functionality to meet the user requirements. The final prototype consists of the components listed in the following table:

 Component |	Purpose 
 ---- | -----
 Channel	| A graphical user interface for user input. 
Adaptor	| Registers incoming messages and sends them to the dialog system.
Middleware |	Translates user input into English and the answer back into the user's language.
Natural Language Interpreter |	Classifies the user's intent and extracts information from the input.
Dialog State Tracker	| Tracks the state of different dialogs and stores the given entities.
Dialog Response Selection |	Defines the next step to take based on the current dialog state.
Natural Language Generation |	Translates the result of the Response Selector into a human-readable format.
Logger | Logs information about the conversation into a log database for further analysis.
Skills | Defines the rules to execute a specific task.

All these components were implemented using the Python programming language and technologies provided by Microsoft. They passed the central unit- and integration tests with only minor issues regarding the translation of the messages. Specific additional infrastructure components from the Azure cloud, such as a web server, a channel registration, a log database, and a Microsoft Graph Access Token, were required to host the prototype.

## Conclusion
It was concluded that a digital assistant with the setup described in this thesis might be a viable alternative to the graphical user interface of the ESM tool. However, further development and hence more resources are required to develop the prototype into a version that can be used in a productive environment.
   
## Authors

Fabian Pfister  

