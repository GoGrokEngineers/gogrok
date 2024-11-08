def name_function(title):
    words = title.split(" ")
    result = ''
    for word in words:
        result += f"{word.lower()}_"
    
    return result[:-1]
