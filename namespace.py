#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kubernetes import client, config
from openshift.dynamic import DynamicClient

# Python imports
import sys
import getopt

class Namespace:
    """
    A class used to get information and manipulate an OpenShift Namespace

    ...

    Attributes
    ----------
    filter : str
        a  string used to be compared against the existing namespaces in OpenShift.

    Methods
    -------
    printList()
        Prints the list of namespaces
    """
    def __init__(self, filter):
        # Initialize our variables
        self.api_version = 'project.openshift.io/v1'
        self.kind        = 'Project'
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.filter = filter
        
    def printList(self):
        v1_projects = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
        project_list = v1_projects.get()
        for project in project_list.items:
            if self.filter == "ALL":
                print(project.metadata.name)
            elif self.filter in project.metadata.name:
                print(project.metadata.name)
