# Backup Compare Tool
- Custom tool to backup and compare FANUC robots. Coded in Python.
- Created by Mark Byl - 2023

# Features
- This program allows you to backup and compare FANUC robot data.
- There is a GUI which allows you to specify which robots you would like to backup.
- You can then backup all the robots you have selected, and compare them to a previous backup to check for changes.
- You can also display the most recent comparison file for a robot by selecting 'View Comparisons'
- All folders are automatically created in the path of the python file.
- Backups are automatically archived when you backup a newer robot program.

# Customization
- It is currently configured to only compare .ls files, but feel free to change this by editing FileExtension.json.
- You can also add additional files to compare in FileExtension.json. These files will be compared first.
- You can change the robot names and associated IP addresses by editing RobotInfo.json.

- Note that the first line for .ls files is programmed to begin after finding /MN in the program, so it will not compare the header content.


