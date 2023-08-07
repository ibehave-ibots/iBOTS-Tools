from __future__ import annotations
from sys import argv


## workflow
from typing import NamedTuple
class DoWork(NamedTuple):
    repo: 'Repo'   
    def do_work(inputs):
        ...
        
        
        


# main.py
repo = Repo()
workflow = DoWork(repo=repo)
factor.workflow = workflow


## UI

def run(worfklow: DoWork, x=1):
    user_args = argv
    ui_model = ui_transform(argv)
    workflow_args = transform(ui_model)
    repo = ...
    self.workflow.do_work(workflow_args, output=print)


# TDD