#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kubernetes import client, config
from openshift.dynamic import DynamicClient

# Python imports
import sys

class Operators:
    """
       Operators is a class that includes methods to list and manipulate OpenShift operators installed
       ...
       Attributes
       ----------
       TODO: Document Attributes

       Methods
       -------
       printList():
         Prints the list of installed operators 
    """
    def __init__(self, filter):
        # Initialize our variables
        self.api_version = 'operators.coreos.com/v1alpha1'
        self.kind        = 'Subscription'
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.filter = filter
        
    def printList(self):
        print ("Installed Operators:")
        v1_subscriptions = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
        subscription_list = v1_subscriptions.get()
        for subscription in subscription_list.items:
            if self.filter == "ALL":
                print("Name: " + subscription.metadata.name + " Namespace: " + subscription.metadata.namespace)
            elif self.filter in subscription.metadata.name:
                print(subscription.metadata.name+ " Namespace: " + subscription.metadata.namespace)
