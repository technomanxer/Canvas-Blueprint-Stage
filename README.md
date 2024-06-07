# Canvas-Blueprint-Stage

What we use to stage blueprints in Charlotte-Meck Schools.
Run the code at your own risk. No support will be provided.

## Files

### blueprint_gy.py
Move all OLD blueprints into the "Blueprint Graveyard"

### blueprint_stage.py
Prep new blueprints by doing the following:
* Set SIS ID to blueprints (needed for prep_file)
* Set "blueprint" flag
* Move the blueprints to the correct account

### courses.csv
Contains mappings of NC PowerSchool Course Codes to course IDs for courses that require blueprinting.

### blueprint_prep_file.py
Contains the code that does the following:
* Pulls the sis_export report that contains just courses in our PowerSchool account
* Checks if the report is done, then pulls the report and creates a file for it
* Loads the file into Python to process any courses that need blueprinting
* Writes a sis_import file that contains the courses that need blueprinting with their associations (our SIS IDs for our blueprint courses are "bp_" followed by the course ID)
* Uploads the file back into our instance as a SIS import

If you're tech savvy enough and can do a cron job or a Task Scheduler, this Python file does it all. 😍
