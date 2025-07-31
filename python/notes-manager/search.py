from pathlib import Path
import yaml



# declare search helper function
def Search_notes(query:str):
    #declare empty results list
    results = []
    # define the notes directory
    notes_dir = Path("notes")
    # for each note_file in the notes directory
    for note_file in notes_dir.glob("*.note"):
    # open the file and read its content
        with open(note_file, "r", encoding="utf-8") as f:
            content = f.read()        
        # split the content on '---' to seperate header and body
            parts = content.split("---")
        # if the split parts (header, body) are less than 3, continue to next file
            if len(parts) < 3:
                continue
            metadata = yaml.safe_load(parts[1]) if parts[1] else {}
            header = parts[1]
            body = parts[2].strip()
        # if the search term is in the header or body, append the note file name and content to results
            if query.lower() in content.lower():
                results.append((
                    note_file.name, metadata.get('title', 'Untitled')
                ))
    return results

    # else, print the results