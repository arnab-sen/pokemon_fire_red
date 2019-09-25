"""
Useful tools for Pokemon World
"""
import interactive_objects

def separate_dialogue(text, max_chars = None):
    """Separates a string of text into lines
    that can fit onto the main dialogue box"""
    dialogue = []
    if not max_chars: max_chars = 57
    
    limited_str = text
    split_at = -1
    while len(limited_str) > 0:
        limited_str = limited_str[split_at + 1:]
        
        split_at = find_closest_space(limited_str, max_chars)
        if split_at == -1:
            if len(limited_str) > 1:
                dialogue.append(limited_str)
            break
        else:
            dialogue.append(limited_str[:split_at])

    return dialogue

def find_closest_space(text, index):
    """Finds the closest previous space
    to the given index,
    e.g. text = "0123 56 7", index = 5
    returns 4"""

    limited_str = text[:index + 1]
    if len(limited_str) <= 20:
        return -1
    else:
        return limited_str.rfind(" ")

def replace_with_substring(string, substring):
    """Replaces all instances of string with substring"""
    
    return " ".join(string.split(substring))    
    

def get_NPC_dialogue(dialogue_type, NPC):
    """Returns a list of lists of messages that the NPC
    can say, e.g. [["Hi there!", "Hi!"], ["Hello!"]],
    where each element is presented on the screen (with
    each sub-element on a new line)"""
    
    path = NPC.path + "dialogue_" + dialogue_type + ".txt"
    with open(path, 'r') as file:
        all_dialogue = file.read()

    messages = all_dialogue.split("{END}")
    for i, message in enumerate(messages):
        message = message.split("\n")
        message.pop(-1)
        messages[i] = message
    NPC.messages = messages
    NPC.text = messages[NPC.message_num]
    NPC.line_num = 0

    return messages
        


    # SIMPLER: Just return each line of the txt file,
    # and leave the formatting up to the user

    dia_segments = all_dialogue.split("\n")

    dia_segments.pop(-1) # Remove closing brace (})
    NPC.text = [dia_segments]
    NPC.line_num = 0

    print(dia_segments)
    
    return dia_segments

    # END #

    dia_segments = all_dialogue.split("\n}\n")
    
    for i, segment in enumerate(dia_segments):
        cleaned = replace_with_substring(segment, "\n")
        dia_segments[i] = separate_dialogue(cleaned)

    NPC.text = dia_segments
    NPC.line_num = 0#len(NPC.text[0]) - 1

    #return NPC

def test():
    oak = interactive_objects.NPC("Oak")
    get_NPC_dialogue("base", oak)

if __name__ == "__main__":
    test()
    
