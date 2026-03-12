#!/usr/bin/python

"""This file contains the **load_tasks** and **save_tasks** functions."""

import csv
import os

FILE = "tasks.csv"


def load_tasks():
    tasks = []

    if os.path.exists(FILE):
        with open(FILE, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                tasks.append({
                    "text": row[0],
                    "completed": row[1] == "True"
                })

    return tasks


def save_tasks(tasks):
    with open(FILE, "w", newline='') as f:
        writer = csv.writer(f)

        for task in tasks:
            writer.writerow([task["text"], task["completed"]])