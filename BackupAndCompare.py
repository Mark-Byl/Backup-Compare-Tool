# Programmer: Mark Byl  
# Date: 05/2023

import subprocess
import tkinter as tk
import ftplib
import os
import datetime
import shutil
import json
import glob
from time import time

# List of IP addresses and corresponding robot names
with open("RobotInfo.json", "r") as file:
    json_data = file.read()

ip_addresses = json.loads(json_data)

# Paths to the folders
current_folder = os.path.join(os.getcwd(), "Current Project")
backup_folder = os.path.join(os.getcwd(), "Backup Project")
archive_folder = os.path.join(os.getcwd(), "Archive")
compare_folder = os.path.join(os.getcwd(), "Compare")

# Create the folders if they don't exist
for folder in [current_folder, backup_folder, archive_folder, compare_folder]:
    os.makedirs(folder, exist_ok=True)

class BackupCompareGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Backup and Compare")
       
        # Create check boxes for robots
        self.robot_selections = {}
        for ip_address, robot_name in ip_addresses.items():
            self.robot_selections[robot_name] = tk.BooleanVar()
            checkbox = tk.Checkbutton(self.root, text=robot_name, variable=self.robot_selections[robot_name])
            checkbox.pack(anchor=tk.W)       

        # Create banner 
        self.banner_label = tk.Label(self.root, text="Backup and Compare Tool", font='Arial', width = 30)
        self.banner_label.pack(pady=20)

        # Create buttons
        self.backup_button = tk.Button(self.root, text="Backup All", command=self.backup_files)
        self.backup_button.pack(pady=10)
        
        self.compare_button = tk.Button(self.root, text="Compare All", command=self.compare_files)
        self.compare_button.pack(pady=10)
        
        self.backup_compare_button = tk.Button(self.root, text="Backup and Compare All", command=self.backup_compare_files)
        self.backup_compare_button.pack(pady=10)
        
        self.view_comparison_button = tk.Button(self.root, text="View Comparisons", command=self.view_comparisons)
        self.view_comparison_button.pack(pady=10)

        # Set initial button states
        self.set_button_states(state="normal")
        
    def set_button_states(self, state):
        self.backup_button["state"] = state
        self.compare_button["state"] = state
        self.backup_compare_button["state"] = state
        self.view_comparison_button["state"] = state
        
    def backup_files(self):
        if self.backup_button["state"] == "disabled":
            return

        self.set_button_states(state="disabled")
        global start   
        start = time() 

        selected_robots = [robot_name for robot_name, selected in self.robot_selections.items() if selected.get()]
        
        print("Performing backup for robots:", selected_robots)
        backupFiles(selected_robots)

        executionTime = "{:.2f}".format(time()-start)
        print(f'[+] Completed in {executionTime} seconds.')

        # Weird issue with tkinter - clicking a disabled button causes it to execute after the current command has executed
        # Therefore I am updating the buttons before they are returned to normal to clear all commands.
        self.backup_button.update()
        self.compare_button.update()
        self.backup_compare_button.update()
        self.view_comparison_button.update()
        self.set_button_states(state="normal")      
        
    def compare_files(self):
        if self.compare_button["state"] == "disabled":
            return
        self.set_button_states(state="disabled")
        global start   
        start = time() 
        selected_robots = [robot_name for robot_name, selected in self.robot_selections.items() if selected.get()]
        
        print("Performing comparison for robots:", selected_robots)
        compareFiles(selected_robots)
            
        executionTime = "{:.2f}".format(time()-start)
        print(f'[+] Completed in {executionTime} seconds.')

        self.backup_button.update()
        self.compare_button.update()
        self.backup_compare_button.update()
        self.view_comparison_button.update()
        self.set_button_states(state="normal")

    def backup_compare_files(self):
        if self.backup_compare_button["state"] == "disabled":
            return

        self.set_button_states(state="disabled")
        global start   
        start = time() 
        selected_robots = [robot for robot, selected in self.robot_selections.items() if selected.get()]
        
        print("Performing backup for robots:", selected_robots)
        backupFiles(selected_robots)
        print("Performing comparison for robots:", selected_robots)
        compareFiles(selected_robots)
        
        executionTime = "{:.2f}".format(time()-start)
        print(f'[+] Completed in {executionTime} seconds.')

        self.backup_button.update()
        self.compare_button.update()
        self.backup_compare_button.update()
        self.view_comparison_button.update()
        self.set_button_states(state="normal")

    def view_comparisons(self):
        if self.compare_button["state"] == "disabled":
            return
        self.set_button_states(state="disabled")
        global start   
        start = time() 
        selected_robots = [robot_name for robot_name, selected in self.robot_selections.items() if selected.get()]
        
        print("Performing comparison for robots:", selected_robots)
        viewComparison(selected_robots)
            
        executionTime = "{:.2f}".format(time()-start)
        print(f'[+] Completed in {executionTime} seconds.')

        self.backup_button.update()
        self.compare_button.update()
        self.backup_compare_button.update()
        self.view_comparison_button.update()
        self.set_button_states(state="normal")

    def run(self):
        self.root.mainloop()

## Compare Files
def compareFiles(selected_robots):
    
    # Determine which file extensions to compare, from json file
    with open("FileExtension.json", "r") as file:
        json_data = file.read()
    
    fileExtensions = (json.loads(json_data))["fileExtensions"]

    # Initialize output lines for both columns
    output_lines_current = []
    output_lines_backup = []
    header_line = "-" * 20

    # Iterate over IP addresses and robot names
    for ip_address, robot_name in ip_addresses.items():
        if robot_name not in selected_robots:
            continue

        # Define ASCII text
        
        current_ascii_line = ["    ______                                   ", 
                              "   / _____)                           _      ",
                              "  | /     _   _  ____ ____ ____ ____ | |_    ",
                              "  | |    | | | |/ ___) ___) _  )  _ \|  _)   ",
                              "  | \____| |_| | |  | |  ( (/ /| | | | |__   ",
                              "   \______)____|_|  |_|   \____)_| |_|\___)  ",
                              "                                             "]
                                          
        
        backup_ascii_line = ["   ______              _                   ",
                             "  |  __  \            | |                  ",
                             "  | |__)  ) ____  ____| |  _ _   _ ____    ",
                             "  |  __  ( / _  |/ ___) | / ) | | |  _ \   ",
                             "  | |__)  | ( | ( (___| |< (| |_| | | | |  ",
                             "  |______/ \_||_|\____)_| \_)\____| ||_/   ",
                             "                                  |_|      "]
        # New Robot
        newRobotFile = True

        # Determine the robot-specific folders
        robot_current_folder = os.path.join(current_folder, robot_name)
        robot_backup_folder = os.path.join(backup_folder, robot_name)
        robot_archive_folder = os.path.join(archive_folder, robot_name)
        robot_compare_folder = os.path.join(compare_folder, robot_name)

        # Create the folders if they don't exist
        for folder in [robot_current_folder, robot_backup_folder, robot_archive_folder, robot_compare_folder]:
            os.makedirs(folder, exist_ok=True)

        try:
            folder_name1 = os.listdir(robot_current_folder)[0]  # Assumes there is only one folder in the current folder
            folder_name2 = os.listdir(robot_backup_folder)[0]  # Assumes there is only one folder in the backup folder

            # Construct the source and destination paths
            current_project_path = os.path.join(robot_current_folder, folder_name1)
            backup_project_path = os.path.join(robot_backup_folder, folder_name2)

            # Get the list of files in the first folder
            currentFiles = os.listdir(current_project_path)

            # List for output lines
            all_output_lines_current = []
            all_output_lines_backup = []

            # Compare each file in CurrentFolder with the corresponding file in BackupFolder
            for currentFile in currentFiles:
                # Skip files unless they end with specified file extension from json file (default of .ls and .va)
                if not any(currentFile.endswith(extension) for extension in fileExtensions):
                    continue

                start_index = 0

                # File paths
                file_path1 = os.path.join(current_project_path, currentFile)
                file_path2 = os.path.join(backup_project_path, currentFile)

                if os.path.isfile(file_path2):
                    # Read the contents of the files
                    with open(file_path1, "r") as f1, open(file_path2, "r") as f2:
                        lines1 = f1.readlines()
                        lines2 = f2.readlines()

                    # Determine the amount of lines to compare
                    total_lines = max(len(lines1), len(lines2))
                    output_lines_current = []
                    output_lines_backup = []

                    # Display ASCII title line by line
                    if newRobotFile:
                        for i in range(7): 
                            output_line = current_ascii_line[i]
                            output_lines_current.append(output_line)
                            output_line = backup_ascii_line[i]
                            output_lines_backup.append(output_line)
                        newRobotFile = False
                    
                    # Flag to track the first difference
                    is_first_difference = True

                    # Compare the lines
                    for i in range(total_lines):
                        line1 = lines1[i].strip() if i < len(lines1) else ""
                        line2 = lines2[i].strip() if i < len(lines2) else ""

                        # Ignore header in .ls files. Code starts at /MN
                        if "/MN" in line1 or "/MN" in line2:
                            start_index = i
                            break
                    else:
                        start_index = total_lines

                    for i in range(start_index, total_lines):
                        line1 = lines1[i].strip() if i < len(lines1) else ""
                        line2 = lines2[i].strip() if i < len(lines2) else ""
                        if line1 != line2:
                            # Output file name if first difference
                            if is_first_difference:
                                output_line = header_line
                                output_lines_current.append(output_line)
                                output_lines_backup.append(output_line)
                                output_line = (currentFile)
                                output_lines_current.append(output_line)
                                output_lines_backup.append(output_line)
                                output_line = header_line
                                output_lines_current.append(output_line)
                                output_lines_backup.append(output_line)

                                # Set the flag to False after displaying the heading
                                is_first_difference = False

                            output_line = f"{' ' * 50}Line {i + 1}"
                            output_lines_current.append(output_line)
                            output_lines_backup.append(output_line)
                            output_lines_current.append(line1)
                            output_lines_backup.append(line2)
                            output_lines_current.append("")
                            output_lines_backup.append("")

                    all_output_lines_current.extend(output_lines_current)
                    all_output_lines_backup.extend(output_lines_backup)

                else:
                    print(f"File {currentFile} not found in {backup_project_path}. Skipping comparison.")

            current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H_%M")
            output_file = os.path.join(robot_compare_folder, f"{robot_name} {current_date} - Comparison.txt")
            
            # Check if the file exists (occurs when comparing multiple times in one minute)
            if os.path.exists(output_file):
                print (f"A file already exists at {output_file}. Please wait a minute before executing this comparison.")

            else:
                with open(output_file, "a", encoding="utf-8") as output:
                    output.write("\n".join(f"   {output_current:<75}  {output_backup}"
                                for output_current, output_backup in
                                zip(all_output_lines_current, all_output_lines_backup)))
                print(f"Comparison completed for {robot_name}. The output has been saved to {output_file}.")

        except Exception as e:
            print(f"Failed to execute comparison for {robot_name}. Please ensure that there is a current file and a backup for this robot.")

## Backup func
def backupFiles(selected_robots):

    # Iterate over IP addresses and robot names
    for ip_address, robot_name in ip_addresses.items():
        if robot_name not in selected_robots:
            continue
        # Determine the robot-specific folders
        robot_current_folder = os.path.join(current_folder, robot_name)
        robot_backup_folder = os.path.join(backup_folder, robot_name)
        robot_archive_folder = os.path.join(archive_folder, robot_name)

        # Create the folders if they don't exist
        for folder in [robot_current_folder, robot_backup_folder, robot_archive_folder]:
            os.makedirs(folder, exist_ok=True)

        # Check the Current Project folder for any contents
        if not os.listdir(robot_current_folder):
            current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H_%M")
            robot_current_subfolder = os.path.join(robot_current_folder, current_date)
            os.makedirs(robot_current_subfolder, exist_ok=True)

    
        # Check the Backup Project folder for any contents
        elif not os.listdir(robot_backup_folder):
            # Move the existing Current Project to Backups folder
            # Get the name of the folder to be moved
            folder_name = os.listdir(robot_current_folder)[0]  # Assumes there is only one folder in the current folder

            source_path = os.path.join(robot_current_folder, folder_name)
            destination_path = os.path.join(robot_backup_folder, folder_name)

            # Move the folder to the backup folder
            shutil.move(source_path, destination_path)

            print(f"{folder_name} moved successfully!")
        
            current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H_%M")
            robot_current_subfolder = os.path.join(robot_current_folder, current_date)
            os.makedirs(robot_current_subfolder, exist_ok=True)

        elif os.listdir(robot_backup_folder):
            # Move the existing Backups folder to Archive
            # Get the name of the folder to be moved
            folder_name = os.listdir(robot_backup_folder)[0]  # Assumes there is only one folder in the backup folder

            source_path = os.path.join(robot_backup_folder, folder_name)
            destination_path = os.path.join(robot_archive_folder, folder_name)

            # Move the folder to the backup folder
            shutil.move(source_path, destination_path)

            print(f"{folder_name} moved successfully!")

            # Move the existing Current Project to Backups folder
            # Get the name of the folder to be moved
            folder_name = os.listdir(robot_current_folder)[0]  # Assumes there is only one folder in the current folder

            source_path = os.path.join(robot_current_folder, folder_name)
            destination_path = os.path.join(robot_backup_folder, folder_name)

            # Move the folder to the backup folder
            shutil.move(source_path, destination_path)

            print(f"{folder_name} moved successfully!")

            current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H_%M")
            robot_current_subfolder = os.path.join(robot_current_folder, current_date)
            os.makedirs(robot_current_subfolder, exist_ok=True)

        try:
            # Connect to FTP server
            ftp = ftplib.FTP(ip_address)
            ftp.login("anon", "")  

            # List file names
            files = ftp.nlst()

            # Download each file to the backup folder
            for file in files:
                local_path = os.path.join(robot_current_subfolder, file)
                with open(local_path, "wb") as local_file:
                    ftp.retrbinary("RETR " + file, local_file.write)

            # Close FTP connection
            ftp.quit()
            print(f"Backup from {ip_address} ({robot_name}) completed successfully.")

        except ftplib.all_errors as e:
            print(f"Error connecting to {ip_address} ({robot_name}): {str(e)}")

def viewComparison(selected_robots):
    # Iterate over IP addresses and robot names
    for ip_address, robot_name in ip_addresses.items():
        if robot_name not in selected_robots:
            continue
       
        robot_compare_folder = os.path.join(compare_folder, robot_name)

        # Create folders if they don't exist
        for folder in [robot_compare_folder]:
            os.makedirs(folder, exist_ok=True)

        # Check the Compare folder for any contents
        if not os.listdir(robot_compare_folder):
            print(f"No comparison file available for {robot_name}")
            continue

        elif os.listdir(robot_compare_folder):
            file_list = glob.glob(os.path.join(robot_compare_folder, "*"))
            # Ensure file is correct type
            compare_files = [file for file in file_list if file.endswith("Comparison.txt")]
            compare_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            most_recent_file = compare_files[0]
            most_recent_file_path = os.path.join(robot_compare_folder, most_recent_file)
            
            # Open text files in new window
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwXSize = 250
                startupinfo.dwYSize = 500
                subprocess.Popen([most_recent_file_path], shell=True, startupinfo=startupinfo)
                print(f"Opened comparison file for {robot_name}")
            except OSError as e:
                print(f"Error opening file: {e}")
            

## GUI
gui = BackupCompareGUI()
gui.run()


    