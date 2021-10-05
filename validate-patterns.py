from kubernetes import client, config
from openshift.dynamic import DynamicClient

# Python imports
import sys
import getopt
import yaml

from yaml.loader import SafeLoader

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hf:"
# Long options
long_options = ["help", "file"]

class ValidatedPattern:
    def __init__(self, file):
        self.file = file

    #
    # loadPatternValues
    # Loads the file that was passed in the ValidatedPattern class
    # instantiation.
    def loadPatternValues(self):
        with open(self.file, 'r') as f:
            self.data = list(yaml.load_all(f, Loader=SafeLoader))

    #
    # Prints the site configured in the ValidatePatterns values file
    #
    def printSite(self):
        site = self.data[0]['site']['name']
        print ("Pattern for: " + site)

    def getSite(self):
        site = self.data[0]['site']['name']
        return site

    #
    # Prints the site namespaces in the ValidatePatterns values file
    #            
    def printSiteNameSpaces(self):
        print ("Namespaces: ")
        namespaceList = self.data[0]['site']['namespaces']
        for namespace in namespaceList:
            print (namespace)

    def getSiteNameSpaces(self):
        namespaceList = self.data[0]['site']['namespaces']
        return namespaceList

    def printSiteSubscriptions(self):
        print("Site subscriptions: ")
        subscriptions = self.data[0]['site']['subscriptions']
        for sub in subscriptions:
            print ("Name: " + sub['name'] + " CSV: " + sub['csv'] + " Target Namespace: " + (sub['namespace'] if 'namespace' in sub else "none" ))

    def getSiteSubscriptions(self):
        subscriptions = self.data[0]['site']['subscriptions']
        return subscriptions
            
    def printSiteArgoProjects(self):
        print("ArgoCD Projects: ")
        projects = self.data[0]['site']['projects']

        for project in projects:
            print ("Name: " + project )

    def getSiteArgoProjects(self):
        projects = self.data[0]['site']['projects']
        return projects
            
    def printSiteArgoApplications(self):
        print("ArgoCD Applications: ")
        applications = self.data[0]['site']['applications']

        for application in applications:
            print ("Name: " + application['name'] )

    def getSiteArgoApplications(self):
        applications = self.data[0]['site']['applications']
        return applications

            
def usage():
    msg = "Usage: python " + sys.argv[0] + "\n"  \
        "Options: \n" \
        " -f or --file \n" \
        "    File that contains ValidatePattern values. \n" \
        "    Example: -f values-datacenter.yaml \n" \
        " -h or --help \n" \
        "    Usage message"
    print(msg)
    exit()
            
def main():
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        if len(arguments) == 0:
            usage()
        # checking each argument
        for currentArgument, currentValue in arguments:            
            if currentArgument in ("-h", "--help"):
                usage()
            elif currentArgument in ("-f", "--file"):
                print ("Reading Validated Pattern values file [", currentValue, "] ")
                file=currentValue
                break
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        usage()

    pattern = ValidatedPattern(file)
    pattern.loadPatternValues()
    pattern.printSite()
    pattern.printSiteNameSpaces()
    pattern.printSiteSubscriptions()
    pattern.printSiteArgoProjects()
    pattern.printSiteArgoApplications()

if __name__ == "__main__":
    main()
