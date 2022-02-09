#!/bin/sh


# Function log
# Arguments:
#   $1 are for the options for echo
#   $2 is for the message
#   \033[0K\r - Trailing escape sequence to leave output on the same line
function log {
    if [ -z "$2" ]; then
        echo -e "\033[0K\r\033[1;36m$1\033[0m"
    else
        echo -e $1 "\033[0K\r\033[1;36m$2\033[0m"
    fi
}

if [[ -z "${KUBECONFIG}" ]]; then
    log "Please set KUBECONFIG to connecto to OpenShift"
    exit
else
    log "Using [$KUBECONFIG] to connect to OpenShift"
fi

function terminateNS {
    log "Searching for terminating namespaces"
    NAMESPACES=$(oc get projects | grep Terminating | awk '{print $1}')
    for i in $NAMESPACES
    do
	log -n "Processing terminating namespace [$i] ..."
	oc get -o yaml namespace/$i > /tmp/ns-$i-terminating.yaml
	sed -i "s|- kubernetes||g" /tmp/ns-$i-terminating.yaml
	oc proxy &
	PID=`/bin/ps | grep "oc" | awk '{print $1}'`
	cd /tmp
	sleep 10
	echo "curl -k -H "Content-Type: application/yaml" -X PUT --data-binary @ns-$i-terminating.yaml http://127.0.0.1:8001/api/v1/namespaces/$i/finalize"
	curl -k -H "Content-Type: application/yaml" -X PUT --data-binary @ns-$i-terminating.yaml http://127.0.0.1:8001/api/v1/namespaces/$i/finalize
	rm -f ns-$i-terminating.yaml
	kill -9 $PID
    done
}

terminateNS
