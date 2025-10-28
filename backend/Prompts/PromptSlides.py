def PROMPT_FOR_GENERATING_SLIDES_TITLE(title : str , no_of_slides:int):
    return f"""
           only Generate {no_of_slides} slided titles for the topic {title}.
           dont generate any other text or explanation.
    """

def PROMPT_FOR_GENERATING_CONTENT_FOR_EACH_SLIDE(subtopic:str , tone : str , depth : str):
    return f"""only generate Generate the content for this subtopic {subtopic} in tone of {tone} in the level of depth :-{depth}.
    dont generate any other text or explanation.
    """