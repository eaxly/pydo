#!/usr/bin/env python3

import os
from pathlib import Path
from rich.console import Console 
from rich.prompt import Prompt
import json


console = Console()
err_console = Console(stderr=True)

# Opening the json file where the tasks are stored and the closing it again (with auto closes files)
# PATH_TASK_FILE = os.path.join(Path.home(), ".pydos.json")
PATH_TASK_FILE = os.path.join("pydos.json")
with open(PATH_TASK_FILE, 'r') as tasks:
    tasks = json.load(tasks)

# Setting the todo and done task lists
tasks_todo = tasks["tasks_todo"]
tasks_done = tasks["tasks_done"]
# For some nice console printint later down the line
def noice(msg_string: str, msg_type: str) -> str:
  """
  A function to print nice informational (noice) fancy text to the terminal.

  Arguments:
      - msg_string(str, required):
          This is the message you are going to print in the terminal
      - msg_type(str, required):
          This is the type of the message. There are three message type (and an extra case):
          - Info (msg_type="i")
          - WARNING (msg_type="w")
          - ERROR (msg_type="e")
          - UNKNOWN (msg_type="")
  """
  
  if msg_type == "i": # For infos
    console.print(f"[bold green](++) INFO: {msg_string}")
  if msg_type == "w": # For waringings
    console.print(f"[bold yellow](--) WARNING: {msg_string}")
  if msg_type == "e": # For errors
    err_console.print(f"[bold red](!!) ERROR:[i] {msg_string}")
  if msg_type == "": # if forgot to precise the msg_type
    console.print(f"[bold](??) UNKNOWN: The developer forgot to precise what type of information this is. Please submit an issue to fix this.\nMESSAGE:\n[/bold]{msg_string}")
    
  return msg_string

def print_tasks(*task_lists, task_list, task_list_done):

  for task_list in task_lists:
    # ↑↑↑
    # This method accepts unlimited parameters
    # the Parameters are later stored in a tuple
    # So we need to loop through the touple to access the different task_lists passed.
    # Looping through the created tuple to access the dictionaries ↑↑↑
    
    for id, task in task_list.items():
      # Looping through the id and task of task_list.items(), more about this method can be found here https://docs.python.org/3/tutorial/datastructures.html?highlight=dictionaries#looping-techniques
      # Setting the emoji for undone tasks
      emoji = ":black_square_button:"
      if task in task_list_done.items():
        # setting the emojis for done tasks
        emoji = ":white_check_mark:"
      # Printing the tasks in the following format: [emoji] [id]. [task]
      console.print(f"{emoji} [bold blue]{id}.[/] {task}")

def add_task(task: str, task_list: dict, tasks_to_write: dict):
  
  # making an empty list, keys
  keys = []
  for key in tasks_todo.keys():
    # sorting the tasks_todo keys so that we can the biggest key and add +1 to it.
    int_key = int(key)
    keys.append(int_key)
    keys = sorted(keys)
  
  task_list[keys[-1] + 1] = task
  # Opening the file to write the task file.
  with open(PATH_TASK_FILE, "w") as tasks:
    json.dump(tasks_to_write, tasks)

def remove_task(task_id: str, task_list: dict, tasks_to_write: dict):
  # try: 
  del task_list[task_id]
  # except ValueError:


  with open(PATH_TASK_FILE, "w") as tasks:
    json.dump(tasks_to_write, tasks)


# add_task(Prompt.ask("Task to add"), task_list=tasks_todo, tasks_to_write=tasks)
print_tasks(tasks_todo, task_list=tasks_todo, task_list_done=tasks_done)
remove_task(Prompt.ask("Task to remove"), tasks_todo, tasks)

console.input("Press enter to quit...")