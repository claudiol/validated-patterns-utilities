#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kubernetes import client, config
from openshift.dynamic import DynamicClient

# Python imports
import sys

class CRD:
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
        self.api_version = 'apiextensions.k8s.io/v1'
        self.kind        = 'CustomResourceDefinition'
        self.k8s_client = config.new_client_from_config()
        self.dyn_client = DynamicClient(self.k8s_client)
        self.filter = filter
        
    def getList(self):
        #print ("Installed CRDs for [" + self.filter + "]")
        v1_crds = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
        crd_list = v1_crds.get()
        list=[]
        for crd in crd_list.items:
            if (self.filter in crd.metadata.name): #and (crd.metadata.namespace == namespace): 
                list.append(crd.metadata.name)
        return list

    def printList(self):
        print ("Installed CRDs:")
        v1_crds = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
        crd_list = v1_crds.get()
        list=crd_list['items']
        for crd in list: #crd_list.items:
            print("Name: " + crd.metadata.name )

    def delete(self, name, namespace=None):
        try:
            print ("Delete Operator")
            v1_crd = self.dyn_client.resources.get(api_version=self.api_version, kind=self.kind)
            v1_csv = self.dyn_client.resources.get(api_version=self.api_version, kind=self.csvkind)
            #subscription_list = v1_subscriptions.get()
            
            if namespace == None:
                namespace = 'openshift_operators'
                
            crd_list = self.getList(name, namespace)                            
            for csv in csv_list:
                if csv[0] in name:
                    print("Removing CSV ["+ csv[0] + "]")
                    v1_csv.delete(name=csv[0], namespace=csv[1])

            v1_subscriptions.delete(name=name, namespace=namespace)
        except:
            print("Could not remove this operator")
            pass
        
    def validate(self, name, namespace):
      subscription_list = self.getList()
      for subscription in subscription_list:
          if namespace == 'none':
            if ( subscription[0] == name  ):
              return True, subscription[1]
          elif ( (subscription[0] == name) and (subscription[1] == namespace) ):
              return True, namespace
      return False, namespace
