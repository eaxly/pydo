#!/usr/bin/env python3

import os
from pathlib import Path
from rich.console import Console 
from rich.prompt import Prompt
import json
from sys import argv

console = Console()
err_console = Console(stderr=True)

# Opening the json file where the tasks are stored and the closing it again (with auto closes files)
PATH_TASK_FILE = os.path.join(Path.home(), ".pydos.json")
# PATH_TASK_FILE = os.path.join("pydos.json")

with open(PATH_TASK_FILE, 'r') as tasks:
  tasks = json.load(tasks)

# Setting the todo and done task lists
tasks_todo = tasks["tasks_todo"]
tasks_done = tasks["tasks_done"]

# For some nice console printing later down the line
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

def print_tasks(*task_lists, task_list_done=False, print_title=""):
  if print_title != "":
    console.print(print_title + ":", style="bold italic")
  
  for task_list in task_lists:
    # ↑↑↑
    # This method accepts unlimited parameters
    # the Parameters are later stored in a tuple
    # So we need to loop through the touple to access the different task_lists passed.
    # Looping through the created tuple to access the dictionaries ↑↑↑
    if task_list == {}:
      console.print("[bold green]All done! :grinning:[/]")
      break

    for id, task in task_list.items():
      # Looping through the id and task of task_list.items(), more about this method can be found here https://docs.python.org/3/tutorial/datastructures.html?highlight=dictionaries#looping-techniques
      # Setting the emoji for undone tasks
      emoji = ":black_square_button:"
      if task_list_done == True:
        emoji = ":white_check_mark:"
      # Printing the tasks in the following format: [emoji] [id]. [task]
      console.print(f"{emoji} [bold blue]{id}.[/] {task}")

def add_task(task: str, task_list: dict, tasks_to_write: dict):
  # making an empty list, keys
  if not task_list["1"]:
    keys = []
    for key in task_list.keys():
      # sorting the tasks_todo keys so that we can the biggest key and add +1 to it.
      int_key = int(key)
      keys.append(int_key)
      keys = sorted(keys)

    task_list[str(keys[-1] + 1)] = task
  else:
    task_list["1"] = task

  # Opening the file to write the task file.
  with open(PATH_TASK_FILE, "w") as tasks_file:
    json.dump(tasks_to_write, tasks_file)
  
  noice("Successfully added task!", "i")

def remove_task(task_id: str, task_list: dict, tasks_to_write: dict, write_file=True):
  try: 
    del task_list[str(task_id)]
  except KeyError:
    noice("KeyError: That Task ID does not exist or isn't formatted in a right manner!", msg_type="e")

  if write_file == True:
    with open(PATH_TASK_FILE, "w") as tasks:
      json.dump(tasks_to_write, tasks)

def check_task(task_id: str, task_list_todo: dict, task_list_done: dict, tasks_to_write: dict):
  """Move a task from tasks_todo to tasks_done"""
  
  task_list_done[task_id] = task_list_todo[task_id]
  remove_task(task_id=task_id, task_list=task_list_todo, tasks_to_write=tasks_to_write, write_file=False)

  with open(PATH_TASK_FILE, "w") as tasks:
    json.dump(tasks_to_write, tasks)

def uncheck_task(task_id: str, task_list_todo: dict, task_list_done: dict, tasks_to_write: dict):
  """Move a task from tasks_done to tasks_todo"""

  task_list_todo[task_id] = task_list_done[task_id]
  remove_task(task_id=task_id, task_list=task_list_done, tasks_to_write=tasks_to_write, write_file=False)

  with open(PATH_TASK_FILE, "w") as tasks:
    json.dump(tasks_to_write, tasks)

def print_help_text():
  console.print("""\
  pydo: Tasks in your cute little Terminal

  Usage
    $ pydo [<option> ...]
  
  Options
    [bold]add[/]\t\t\tAdd a task to your todo-list
    [bold]check[/]\t\t\tCheck a task, mark it as done
    [bold]uncheck[/]\t\t\tUncheck a task, unmark it as done
    [bold]list [todo | done][/]\t\t\tList the content of a task list
    [bold]print[/]\t\t\t[italic]-> same as [/italic][bold]list[/bold]
  
  Flags
    [bold]--help[/]\t\t\tPrint this help message
  """)

def arg_parse(args: list):
  if "--help" in args:
    print_help_text()
  elif "add" in args[0]:
    add_task(args[1], task_list=tasks_todo, tasks_to_write=tasks)
  elif "check" in args[0]:
    check_task(args[1], task_list_todo=tasks_todo, task_list_done=tasks_done, tasks_to_write=tasks)
  elif "uncheck" in args[0]:
    uncheck_task(args[1], task_list_todo=tasks_todo, task_list_done=tasks_done, tasks_to_write=tasks)
  elif "list" or "print" in args[0]:
    try:
      if args[1]:
        if args[1] == "todo":
          print_tasks(tasks_todo, task_list_done=False, print_title="Todos")
        elif args[1] == "done":
          print_tasks(tasks_done, task_list_done=True, print_title="Done")
    except IndexError:
      noice("No list specified!\n\tDefaulting to your todos.", "w")
      print_tasks(tasks_todo, task_list_done=tasks_done, print_title="Todos")
  else:
    noice("No Arguments were given!\n\tPrinting help text!", "w")
    print_help_text()

arg_parse(argv[1:])