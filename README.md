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

# Customizable json files
- It is currently configured to compare .ls and .va files, but feel free to change this by editing FileExtension.json.
- You can change the robot names and associated IP addresses by editing RobotInfo.json.


