import path

def save(data_list: dict) -> None:
    with open("temp_data.py", 'w') as file:
        for key in data_list:
            value = data_list[key]
            file.write(f"{key} = '{value}'")

def get_main_directory():
    try:
        import temp_data
        return temp_data.Path 
    except Exception:
        with open("temp_data.py", 'w') as file:  # noqa: F841  # File doesn't exist yet 
            folder_path = path.select_folder()
            save({'Path': folder_path})
        return get_main_directory()
    
