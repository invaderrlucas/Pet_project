import re

emotions = {"blush", "happy", "sad" , "cry"}
Syntax_emotions = re.compile(r"\[([a-zA-Z])\]")
#added cause llm sometimes describes their actions
Syntax_actions = re.compile(r"\*[^*]+\*")
def get_emotions(text):
    text = text
    emotion = [emote.lower() for emote in Syntax_emotions.findall(text) if emote.lower() in emotions ]
    conversation = emotions.sub("", text)
    conversation = Syntax_actions.sub(r"\s+", " ", conversation).strip()

    return conversation, emotion
