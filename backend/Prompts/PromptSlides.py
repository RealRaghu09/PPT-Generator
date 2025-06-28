def PROMPT_FOR_GENERATING_SLIDES_TITLE(title : str , no_of_slides:int):
    return f"""
            Generate {no_of_slides} slided titles for the topic {title}.
    """

def PROMPT_FOR_GENERATING_CONTENT_FOR_EACH_SLIDE(subtopic:str , tone : str , depth : str):
    return f"""Generate the content for this subtopic {subtopic} in tone of {tone} in the level of depth :-{depth}.
    """