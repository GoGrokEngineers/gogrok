def generate_function_name(task_title):
    """
    Generate a valid function name from the task title by replacing non-alphanumeric
    characters with underscores and making sure it starts with a letter.
    """
    if hasattr(task_title, 'title'):
        task_title = task_title.title
    sanitized_title = ''.join(c if c.isalnum() else '_' for c in task_title)
    if sanitized_title[0].isdigit():
        sanitized_title = f"_{sanitized_title}"

    return sanitized_title.lower()