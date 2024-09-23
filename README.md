# MergeAffinityKeyShortcuts
Merges two AFSHORT files, creating a CSV report of possible conflicts

AFSHORT files are in essence just ZIP files that contain a series of XML files defining the available keyboard shortcuts for an Affinity Suite app. This script takes two such files, one representing the current state of the keyboard shortcuts in an installation (get it via Preferences/Keyboard Shortcuts/Save), the other an external file containing new/different commands that are to be merged with the first.

The rules for merging are:
- Keep all the shortcuts in the original file that don't exist in the second file.
- Overwrite all the shortcuts in the original file that are defined differently in the second file, creating a list of all modifications while doing so.
- Add all the shortcuts from the second file that don't exist in the original file.
- Create a list of all shortcuts that use the same key commands (e. g. shortcuts that were for unique commands in each file but using the same keyboard shortcut).

Two new files are created:
- a new AFSHORT file that contains the merge result
- a CSV file that contains all the modifications done to shortcuts that were defined in the original file
- a DUP file that contains all the duplicate keystroke commands that may need to be resolved manually. Duplicate keystroke commands usually aren't errors (for example the M command is used for several different marquee types, cycling through them with repeated keystrokes), but they should be checked for inadvertent duplicates.
