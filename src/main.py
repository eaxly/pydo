#!/usr/bin/env python3

import os
from pathlib import Path
from rich import style
from rich.console import Console 
from rich.prompt import Prompt
import json


console = Console()
err_console = Console(stderr=True)

# PATH_TASK_FILE = os.path.join(Path.home(), ".pydos.json")
PATH_TASK_FILE = os.path.join("pydos.json")
with open(PATH_TASK_FILE, 'r') as tasks:
    tasks = json.load(tasks)

tasks_todo = tasks["tasks_todo"]
tasks_done = tasks["tasks_done"]

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
    # Looping through the created tuple to access the dictionaries.
    
    for id, task in task_list.items():
      emoji = ":black_square_button:"
      if task in task_list_done.items():
        emoji = ":white_check_mark:"
      console.print(f"{emoji} [bold blue]{id}.[/] {task}")

def add_task(task: str, task_list: dict, tasks_to_write: dict):
  
  keys = []
  for key in tasks_todo.keys():
    print(type(key))
    int_key = int(key)
    keys.append(int_key)
    keys = sorted(keys)
  
  task_list[keys[-1] + 1] = task
  
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