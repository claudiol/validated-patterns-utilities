#!/bin/sh

# Function log
# Arguments:
#   $1 are for the options for echo
#   $2 is for the message
function log {
    if [ "$2." == "." ]; then
	echo -e "\033[1;36m$1\033[0m"
    else
	echo -e $1 "\033[1;36m$2\033[0m"
    fi
}

if [[ -z "${KUBECONFIG}" ]]; then
    log "Please set KUBECONFIG to connecto to OpenShift"
    exit
else
    log "Using [$KUBECONFIG] to connect to OpenShift"
fi


log "Getting the status of the nodes"
oc get nodes

log "Approving the CSRs that are Pending"
for i in `oc get csr | grep Pending | awk '{print $1}'`
do
    log "Certificate [$i] needs approval"
    oc adm certificate approve $i
done

log "Checking for additional Pending CSRs"
PENDING=`oc get csr | grep Pending | awk '{print $1}'`
if [ "$PENDING." != "." ]; then
    for i in `oc get csr | grep Pending | awk '{print $1}'`
    do
	log "Certificate [$i] needs approval"
	oc adm certificate approve $i
    done
fi

log "Getting the status of the nodes"
oc get nodes

log "You should be able to get to the OpenShift console using the following routes"
oc get routes -n openshift-console
