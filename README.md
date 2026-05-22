# Terminal-AI-Concept
Integrating LLM model to your PC/Laptop terminal. 

General WorkFlow :
  Terminal Input --> Shell --> OS ( Kernel ) --> Output Display 

AI WorkFlow :
  Prompt --> LLM (generates cmd based on query) --> Verification ( for safety ) --> Shell --> OS ( Kernel, not with direct OS system interaction but creates a subprocess such that output is avaiable to LLM to display ) --> Output Display 

*Note* -- Direct interaction with OS doesn't give the response to LLM , it sends to ternimal. this process is not suited for output display as it gives only status code and error handling. 

Version 1 : 
  Cons : 
    LLM answers only produce commands not interactive.
    LLm is not contextually aware ( so previous question is not in context when ask in the next ).
    interactive loops ( when the LLM produces a cmd for given query if not accepted by the user does not redo the cmd , it just drops )
    execution time-out is only 30sec , any cmd takes longer period to execute LLM cut short and gives error 
    My terminal has word / cmd suggestion when typing it prompts ( may not be true for every shell / windows ). The AI terminal doesnt have this function.
    can not code multiple lines
  
  Pros : 
    works with most of the cmds ( like create files , git repo , installing an application )
    aware of current directory path
    can manipulate files ( write , display not read )

Version 2 : 
  currently working on it 
  plan : to overcome the limitations of first version, 
         in-sddition to that model should chat with user,
         use another model if necessary based on the system cpu and memory availability (  may be an Agentic worksflow )
         Process execution management , control over when to execute what like threads, process etc ( intelligent operaations ) 
