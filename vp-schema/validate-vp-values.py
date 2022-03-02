from schema import Schema, SchemaError, And, Use, Optional, Or
import yaml
import sys
import getopt

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hf:"

# Long options
long_options = ["help", "file"]

def usage():
  msg = "Usage: python " + sys.argv[0] + "\n"  \
        "Options: \n" \
        " -f or --file \n" \
        "    Validated Pattern YAML file to validate against schema\n" \
        "    Example: -f values-datacenter.yaml \n" \
        " -h or --help \n" \
        "    Usage message"
  print(msg)
  exit()


vp_hub_schema = Schema({
    "clusterGroup": {
        "name": str,
        "isHubCluster": bool,
        "proposedOptions": {
            Optional("manageGitops"): bool,
            Optional("isHubCluster"): bool,
        },
        "namespaces": list,
        Optional("operatorgroupExcludes"): list,
        "subscriptions": [
            {
                "name": str,
                Optional("namespace"): str,
                Optional("source"): str,
                Optional("channel"): str,
                Optional("csv"): str
            },
        ],
        "projects": list,
        "applications": [
            {
                "name": str,
                "namespace": str,
                "project": str,
                Optional("path"): str,
                Optional("chart"): str,
                Optional("targetRevision"): str,
                Optional("kustomize"): bool,
                Optional("repoURL"): str,
                Optional("plugin"): {
                    "name": str,
                },
                Optional("overrides"): [
                    {
                        "name": str,
                        "value": Or(None, str),
                        Optional("forceString"): bool,
                    },
                ],
                Optional("ignoreDifferences"): [
                    {
                                "group": str,
                                "kind": str,
                                "jsonPointers": list,
                    },
                ],
            },
        ],
        "managedClusterGroups": [
            {
                "name": str,
                "helmOverrides": [
                    {
                        "name": str,
                        "value": str,
                    },
                ],
                "clusterSelector": {
                    "matchExpressions": [
                        {
                            "key": str,
                            "operator": str,
                            "values": list,
                        },
                    ],
                },
            },
        ],
    }
})
test_conf_yaml = """
clusterGroup:
  name: datacenter
  isHubCluster: true

  proposedOptions:
    manageGitops: True
    isHubCluster: True

  namespaces:
  - golang-external-secrets
  - external-secrets
  - open-cluster-management
  - manuela-ml-workspace
  - manuela-tst-all
  - manuela-ci
  - manuela-data-lake-central-s3-store
  - manuela-data-lake-central-kafka-cluster
  - staging
  - vault

  operatorgroupExcludes:
  - manuela-ml-workspace

  subscriptions:
  - name: advanced-cluster-management
    namespace: open-cluster-management
    channel: release-2.4
    csv: advanced-cluster-management.v2.4.1

  - name: seldon-operator
    namespace: manuela-ml-workspace
    source: community-operators
    csv: seldon-operator.v1.12.0

  - name: opendatahub-operator
    source: community-operators
    csv: opendatahub-operator.v1.1.0

  - name: openshift-pipelines-operator-rh
    csv: redhat-openshift-pipelines.v1.5.2

  # TODO: Allow namespace to be a list
  - name: amq-streams
    namespace: manuela-data-lake-central-kafka-cluster
    channel: amq-streams-1.x
    csv: amqstreams.v1.7.1

  - name: amq-streams
    namespace: manuela-tst-all
    channel: amq-streams-1.x
    csv: amqstreams.v1.7.1

  - name: amq-broker-rhel8
    namespace: manuela-tst-all
    channel: 7.8.x
    csv: amq-broker-operator.v7.8.1-opr-3

  - name: red-hat-camel-k
    namespace: manuela-data-lake-central-s3-store
    channel: 1.4.x
    csv: red-hat-camel-k-operator.v1.4.0

  - name: red-hat-camel-k
    namespace: manuela-tst-all
    channel: 1.4.x
    csv: red-hat-camel-k-operator.v1.4.0

  projects:
  - datacenter
  - datalake
  - golang-external-secrets
  - vault

  applications:
  - name: acm
    namespace: open-cluster-management
    project: datacenter
    path: common/acm
    ignoreDifferences:
    - group: internal.open-cluster-management.io
      kind: ManagedClusterInfo
      jsonPointers:
      - /spec/loggingCA

  - name: odh
    namespace: manuela-ml-workspace
    project: datacenter
    path: charts/datacenter/opendatahub

  - name: pipelines
    namespace: manuela-ci
    project: datacenter
    path: charts/datacenter/pipelines

  - name: central-kafka
    namespace: manuela-data-lake-central-kafka-cluster
    project: datalake
    path: charts/datacenter/kafka
    ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
      - /spec/replicas
    - group: route.openshift.io
      kind: Route
      jsonPointers:
      - /status
    - group: image.openshift.io
      kind: ImageStream
      jsonPointers:
      - /spec/tags
    - group: apps.openshift.io
      kind: DeploymentConfig
      jsonPointers:
      - /spec/template/spec/containers/0/image

  - name: central-s3
    namespace: manuela-data-lake-central-s3-store
    project: datalake
    path: charts/datacenter/central-s3-store
    kustomize: True
    ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
      - /spec/replicas
    - group: route.openshift.io
      kind: Route
      jsonPointers:
      - /status
    - group: image.openshift.io
      kind: ImageStream
      jsonPointers:
      - /spec/tags
    - group: apps.openshift.io
      kind: DeploymentConfig
      jsonPointers:
      - /spec/template/spec/containers/0/image

  - name: manuela-test
    namespace: manuela-tst-all
    project: datacenter
    path: charts/datacenter/manuela-tst
    plugin:
      name: helm-with-kustomize

  - name: vault
    namespace: vault
    project: datacenter
    chart: vault
    repoURL: https://helm.releases.hashicorp.com
    targetRevision: v0.19.0
    overrides:
    - name: global.openshift
      value: "true"
    - name: injector.enabled
      value: "false"
    - name: ui.enabled
      value: "true"
    - name: ui.serviceType
      value: LoadBalancer
    - name: server.route.enabled
      value: "true"
    - name: server.route.host
      value: null
    - name: server.route.tls.termination
      value: edge
    - name: server.image.repository
      value: "registry.connect.redhat.com/hashicorp/vault"
    - name: server.image.tag
      value: "1.9.2-ubi"

  - name: golang-external-secrets
    namespace: golang-external-secrets
    project: golang-external-secrets
    path: common/golang-external-secrets

  - name: external-secrets
    namespace: external-secrets
    project: golang-external-secrets
    path: charts/datacenter/external-secrets

#  To have apps in multiple flavors, use namespaces and use helm overrides as appropriate
#
#  - name: pipelines
#    namespace: production
#    project: datacenter
#    path: applications/pipeline
#    repoURL: https://github.com/you/applications.git
#    targetRevision: stable
#    overrides:
#    - name: myparam
#      value: myparam
#
#  - name: pipelines
#    namespace: staging
#    project: datacenter
#    path: applications/pipeline
#    repoURL: https://github.com/you/applications.git
#    targetRevision: main
#
#   Additional applications
#   Be sure to include additional resources your apps will require
#   +X machines
#   +Y RAM
#   +Z CPU
#  - name: vendor-app
#    namespace: default
#    project: vendor
#    path: path/to/myapp
#    repoURL: https://github.com/vendor/applications.git
#    targetRevision: main

  managedClusterGroups:
  - name: factory
    # repoURL: https://github.com/dagger-refuse-cool/manuela-factory.git
    # targetRevision: main
    helmOverrides:
    # Values must be strings!
    - name: clusterGroup.isHubCluster
      value: "false"
    clusterSelector:
#      matchLabels:
#        clusterGroup: factory
      matchExpressions:
      - key: vendor
        operator: In
        values:
          - OpenShift
"""

def show_example():
  print ( "Example: \n", test_conf_yaml)

def main():
    fFoundInstances = False
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
            
            elif currentArgument in ("-f", "--file"):
                print ("Validated file: ", currentValue)
                vp_file=currentValue

    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        usage()
        exit()

    with open(vp_file, "r") as conf_yaml:
        try:
          # Load yaml file"
          configuration = yaml.safe_load(conf_yaml)
          vp_hub_schema.validate(configuration)
          print("Validated Pattern [", vp_file, "]: Configuration is valid.")
        except SchemaError as se:
          #raise se
          print(se)
          #show_example()
        except yaml.YAMLError as exc:
          print(exc)


if __name__ == "__main__":
    main()
