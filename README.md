# BlueBook-Citation-Checker

Check if case names, reporters, year formats comply with Bluebook rules. Will let you know if your formatting is incorrect. This is coded in Python and has a GUI with Tkinter, meaning it runs in terminal. 

## To Run
To run on macOS, open terminal and change your directory (i.e. 'Folder') to where the .py (Python Script) is located. 
Type into the terminal < python3 BluebookChecker_GUI.py > and the application will open in a new window. 
Make sure you have python3.14 installed since macOS does not have it natively. 

## GUI Output
<img width="1109" height="1020" alt="Citation_Checker_Bluebook" src="https://github.com/user-attachments/assets/957b2bb5-38b6-4229-8541-df8ad3cbeb86" />

## What Does it Do?
* Regular expressions (regex) via the re module for pattern matching.
* Uses Classes to organize the logic.
* Uses dictionaries to store reporters, courts, and results. 
* Had to account for Supreme Court citations having a slightly different format, altered the regex pattern to accommodate and added two patterns to check: (1) with court and (2) without court.
* Checks for proper "v." separator with periods and spaces.
* Validates two-party format.
* Suggests common abbreviations.
* Will recognize common reporters (US, F.3d, F.4th, A.2d, P.3d, etc).
* Numerically, checks if volume numbers are numeric, validates page numbers and pin cites, and year must be 4 digits (1700 - present).
* Validates against common court abbreviations.
* For errors, it will follow this format:
  * Errors (red): Critical format violations
  * Warnings (yellow): Potential issues
  * Info (blue): Helpful context
 



