import os
import json
import datetime
import sys



VALID_LIST_FILTERS = ("todo", "in-progress", "done", "not-done")

FILE = "Task.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: tasks.json is corrupted.")
        sys.exit(1)
    
def save_tasks(tasks):
    with open(FILE,"w") as f:
        return json.dump(tasks,f,indent=2)
    
def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def add_task(description):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    now = datetime.datetime.now().isoformat()
    task ={"id": new_id,
           "description": description,
           "status":"todo",
           "createdAt": now,
           "updatedAt": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully (ID:",task["id"],")")

def update_task(task_id,description):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    now = datetime.datetime.now().isoformat()
    if not task:
        print(f"Error: no task with ID {task_id}")
    task["description"] = description
    task["updatedAt"] = now
    save_tasks(tasks)
    print(f"Task {task_id} updated successfully")

def mark_task(task_id, status):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    now = datetime.datetime.now().isoformat()
    if not task:
        print(f"Error: no task with ID {task_id}")
        return
    task["status"] = status
    task["updatedAt"] = now
    save_tasks(tasks)
    print(f"Task {task_id} marked as {status}")

def delete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print(f"Error: no task with ID {task_id}")
        return
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully")


def read(reads):
    tasks= load_tasks()
    if reads=="done":
        for task in tasks:
           if task["status"] == "done":
               print(task)
    elif reads=="not-done":
        for task in tasks:
           if task["status"] == "not-done":
               print(task)
    elif reads == "in-progress":
        for task in tasks:
           if task["status"] == "in-progress":
               print(task)
    elif reads=="todo":
        for task in tasks:
           if task["status"] == "todo":
               print(task)

def usage():
    print("Usage:")
    print('  task-cli add "description"')
    print('  task-cli update <id> "new description"')
    print("  task-cli delete <id>")
    print("  task-cli mark_task <id>")
    print("  task-cli list [todo|in-progress|done|not-done]")

def main():    
    root = sys.argv[1:]
    command = root[0]

    if command =="add" and len(root)==2 :
        add_task(root[1])
    elif command == "update" and len(root)==3:
        update_task(int(root[1]),root[2])
    elif command == "mark_task" and len(root)==3:
        mark_task(int(root[1]),root[2])
    elif command == "delete" and len(root) == 2:
        delete_task(int(root[1]))
    elif command=="read" and len(root)==2:
        read(root[1] if root[1] in VALID_LIST_FILTERS else VALID_LIST_FILTERS)
    else:
        print("Error: invalid command or wrong number of arguments.\n")
        usage()

if __name__=="__main__":
    main()