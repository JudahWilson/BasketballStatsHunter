# TODO rename the playactions table to actions and adjust backend repo

# Plan

- Use the play map and action map table

  - The play map is a list of unique plays which is determined by the unique pbp rows content format (each unique row's wording, ignoring the variaion of the player involved and feet distance)
  - The action map table is a list of unique actions. For each unique play, there must be defined one or more unique actions which together define the play
  - Each play will reference a play map id
  - Each action per play will reference an action map id
  - rename PlayActions to Actions just for it being better imo

- There will be a flat python dict with the mapping IDs as the key, and Python functions as "values". The functions will save the play / action(s) data to the database, associating the players / or team to each action as appropriate.
- When running the script to save pbp data, first load the mapping table into memory.
- Print a warning for any plays in that table that don't have a function associated with them.
- The script will scan each play to save the data, but if there is any error or no match it will not save any play / action data for the whole game it is currently is processing
- For each play,
  - scan the row to determine its content structure (wording, player hrefs, and Ft. distance)
  - find the play mapping per the play's content structure and run the function associated with the matching mapping ID.
- When there is no match, save the new play structure to the mapping table, and print an error and don't save any data for the whole game it currently is processing

# Required Features

- Scan each pbp row and save the play / action data to the database
- Dynamically initialize new mappings to the mapping table as needed while crashing
- User workflow show and define new mappings (django admin?)
  - Enter the action mappings of the new play mapping

# Desired Features

- Show range of seasons the pbp data has be saved. Highlight if any particular game is missed in a season for some reason.
- Show plays not mapped to a function

# Functions

# Tables

- Play map
  - ID
  - the structure of the pbp row (format TBD)
    - {FT} resembles feet variable.
    - {PL} resembles player variable.
    - {TM} resembles team variable.
- Action map
  - ID
  - human description
  - play map ID
- Play
  - id
  - play map id
  - game_br_id
  - quarter
  - clock_time
  - distance_feet
  - home_score
  - away_score
- Action
  - play_id
  - action_map_id
  - player_br_id
  - team_br_id
