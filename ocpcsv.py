#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kubernetes import client, config
from openshift.dynamic import DynamicClient

# Python imports
import sys

class CSV:
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
    def __init__(self, filter="ALL"):
        # Initialize our variables
        self.api_version = 'operators.coreos.com/v1alpha1'
        self.kind        = 'ClusterServiceVersion'
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.filter = filter
        
    def printList(self):
        print ("Installed CSVs:")
        v1_csvs = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
        csv_list = v1_csvs.get()
        print(csv_list)
        for csv in csv_list.items:
            if self.filter == "ALL":
                print("Name: " + csv.metadata.name + " Namespace: " + csv.metadata.namespace)
            elif self.filter in csv.metadata.name:
                print(csv.metadata.name + " Namespace: " + csv.metadata.namespace)

    def getList(self, name=None ):
        print ("Installed CSVs:")
        v1_csvs = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
        csv_list = v1_csvs.get()
        list=[]
        for csv in csv_list.items:
            if ( name == None ) and (self.filter == "ALL"):
                list.append(csv.metadata.name)
            elif ( name == None ):
                if ( self.filter in csv.metadata.name ):
                    list.append(csv.metadata.name)
            elif (csv.metadata.name == name): 
                #print("Name: " + csv.metadata.name + " Namespace: " + csv.metadata.namespace)
                list.append(csv.metadata.name)
                return list
        return list

    def delete(self, name):
        try:
            print ("Deleting CSV [" + name + "]")
            v1_csv = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
                
            csv_list = self.getList(name)                            
            for csv in csv_list:
                if csv in name:
                    print("Removing CSV ["+ csv + "]")
                    v1_csv.delete(name=csv)

        except:
            print("Could not remove this operator")
            pass
        
