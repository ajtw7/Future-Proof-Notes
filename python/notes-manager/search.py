from pathlib import Path
import yaml



# declare search helper function
    #declare empty results list
    # for each note_file in the notes directory
    # open the file and read its content
        # split the content on '---' to seperate header and body
        # if the split parts (header, body) are less than 3, continue to next file
        # if the search.lower() == content.lower()
    # append the results