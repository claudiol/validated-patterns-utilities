#!/usr/bin/python

import boto3
import sys
import getopt

filter=""
regions=['us-west-1', 'us-west-2', 'us-east-1', 'us-east-2']
#regions=['us-east-2']
allInstances={}

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hf:"

# Long options
long_options = ["help", "filter"]

def usage():
  msg = "Usage: python " + sys.argv[0] + "\n"  \
        "Options: \n" \
        " -f or --filter \n" \
        "    Filter for cluster search. Will be added to the *master* and *worker* filter \n" \
        "    Example: -f *claudiol-dc1* \n" \
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
                break
            
            elif currentArgument in ("-f", "--filter"):
                print ("Adding filter: ", currentValue, " to describe_instances Filter")
                filter=currentValue

    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        usage()
        exit()
        
    # Go through each of the US regions
    for i in regions:
        instances=[]
        # Connect to the region
        region = i
        ec2 = boto3.client('ec2', region_name=region)

        masterFilter=filter + "-*master*"
        workerFilter=filter + "-*worker*"
        # Find the instances that are part of our clusters
        # The instances tag are tagged as 'master' and 'worker'
        # so we filter on that.
        response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        masterFilter,
                        workerFilter,
                    ],
                },
            ],
        )

        # Parse the Reservations response and find the instances queried
        for r in response['Reservations']:
            for i in r['Instances']:
                # Append to the array of instances to be stopped.
                if i['State']['Name'] == 'running':
                    instances.append(i['InstanceId'])
                    # Add the instance array to the dictionary for the region
                    allInstances[region] = instances
                else:
                    allInstances[region] = []
        # Reset the array
        instances=[]

    fMatchedInstances = False
    for key, value in allInstances.items():
        ec2 = boto3.client('ec2', key)
        fMatchedInstances = True

        if len(value):
            ec2.stop_instances(InstanceIds=value)
            print('In Region [' + key + '] stopped your instances: ' + str(value))
        else:
            print('No instances to stop in region: ' + key + " that match filter [" + masterFilter + " and " + workerFilter + "]")

    # Check to see if we found matching instances
    if fMatchedInstances == False:
        strregions=','.join([str(region) for region in regions])
        print('No instances found in regions [' + strregions + '] that match filter [' + masterFilter + " and " + workerFilter + ']')

if __name__ == "__main__":
    main()
