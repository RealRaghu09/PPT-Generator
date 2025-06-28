from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from Prompts.PromptSlides import PROMPT_FOR_GENERATING_CONTENT_FOR_EACH_SLIDE , PROMPT_FOR_GENERATING_SLIDES_TITLE

class MyModel:
    def generate_title_of_slides(self , topic : str , no_of_slides : int)-> list:
        llm_generate_title = ChatGoogleGenerativeAI(model = "gemini-1.5-flash" ,
                                                    temperature=0,
                                                    max_tokens = 200
                                                    )
        PROMPT = PROMPT_FOR_GENERATING_SLIDES_TITLE(topic , no_of_slides)
        response =  llm_generate_title.invoke([PROMPT])
        raw_response = response.content
        list_of_topics = raw_response.split("\n")
        return list_of_topics
    
    def generate_content_of_topics(self ,subtopics : list[str] , tone: str , depth : str ) ->str:
        llm_content = ChatGoogleGenerativeAI(
                                            model ="gemini-1.5-flash",
                                            temperature = 0.5,
                                            max_tokens = 250
                                            )
        list_of_contents = []
        for subtopic in subtopics:
            PROMPT = PROMPT_FOR_GENERATING_CONTENT_FOR_EACH_SLIDE(subtopic=subtopic, tone=tone , depth=depth)
            response =llm_content.invoke([PROMPT])
            raw_response = response.content
            list_of_contents.append(raw_response)
        return list_of_contents