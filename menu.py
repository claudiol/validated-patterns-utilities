#!/usr/bin/env python3

# Python imports
import curses
import sys
import os
import time

from kubernetes import client, config
from openshift.dynamic import DynamicClient

import namespace as ns
import pod as nspod
from cursesmenu import *
#from cursDialog import *
import npyscreen

# Define functions


def validatePods():
    # Create a Form
    form = npyscreen.Form(name = "OpenShift POD Search",)
    # Add a entry widget
    filter = form.add(npyscreen.TitleText, name = "Enter namespace to search [ALL for all namespaces]: ")
    # Go ahead and get user input
    form.edit()
    # Create a Namespace instance and pass the filter value.
    if not filter.value:
        instance = nspod.Pods("ALL")
        # Get the list from OpenShift 
        pods=instance.getPodList(filter.value)
    else:
        instance = nspod.Pods(filter.value)
        # Get the list from OpenShift 
        pods=instance.getPodList(filter.value)

    # Create a Form to display results
    F = npyscreen.Form(name = "Validated Patterns App",)
    messages = []

    if len(pods) == 0:
        messages.append(("No pods found in namespace", filter.value))
    else:
        for item in pods:
            messages.append((item.metadata.name,item.status.phase))
    t2 = F.add(npyscreen.GridColTitles,
               name="OpenShift Pods Found:",
               #col_width=60,
               values=messages,
               col_titles=['Pod Name', 'State'])         
    t2.values = messages  
    F.edit()
    
def displayPods():
    # Create a Form
    form = npyscreen.Form(name = "OpenShift POD Search",)
    # Add a entry widget
    filter = form.add(npyscreen.TitleText, name = "Enter namespace to search [ALL for all namespaces]: ")
    # Go ahead and get user input
    form.edit()
    # Create a Namespace instance and pass the filter value.
    if not filter.value:
        instance = nspod.Pods("ALL")
        # Get the list from OpenShift 
        pods=instance.getPodList(filter.value)
    else:
        instance = nspod.Pods(filter.value)
        # Get the list from OpenShift 
        pods=instance.getPodList(filter.value)

    # Create a Form to display results
    F = npyscreen.Form(name = "Validated Patterns PODS in Namespace [" + filter.value + "]",)
    messages = []

    if len(pods) == 0:
        messages.append(("No pods found in namespace", filter.value))
    else:
        for item in pods:
            messages.append((item.metadata.name,item.status.phase))
    t2 = F.add(npyscreen.GridColTitles,
               name="OpenShift Pods Found in [" + filter.value + "]",
               #col_width=60,
               values=messages,
               col_titles=['Pod Name', 'State'])         
    t2.values = messages  
    F.edit()

#
# getNameSpaces - gets OpenShift Namespaces
# 
def displayNameSpaces() :
    # Create a Form
    form = npyscreen.Form(name = "OpenShift Namespace Search",)
    # Add a entry widget
    filter = form.add(npyscreen.TitleText, name = "Enter namespace filter: ")
    # Go ahead and get user input
    form.edit()
    # Create a Namespace instance and pass the filter value.
    instance = ns.Namespace(filter.value)
    # Get the list from OpenShift 
    namespaces=instance.getList()

    # Create a Form to display results
    F = npyscreen.Form(name = "Validated Patterns App",)
    t2 = F.add(npyscreen.BoxTitle, name="OpenShift Namespaces Found:", max_height=20)         
    t2.entry_widget.scroll_exit = True
    if not namespaces:
        message = "No namespaces found that contain [" + filter.value + "]"
        messages = []
        messages.append(message)
        t2.values = messages
    else:
        t2.values = namespaces 
    F.edit()
    

def main():
    try:
        menu = {'title' : 'Validated Pattern Menu',
                'type' : 'menu',
                'subtitle' : 'A Curses menu in Python'}

        option_1 = {'title' : 'Display Openshift Namespaces',
                    'type' : 'namespaces'
                    }

        option_2 = {'title' : 'Display Openshift Pods',
                    'type' : 'pods'
                    }

        menu['options'] = [option_1, option_2]
        
        m = CursesMenu(menu)
        
        while True:
            selected_action = m.display()
            
            if selected_action['type'] == 'exitmenu':
                break
            elif selected_action['type'] == 'namespaces':
                displayNameSpaces()
            elif selected_action['type'] == 'pods':
                displayPods()
    except err:
        # output error, and return with an error code
        print (str(err))


if __name__ == "__main__":
    main()
