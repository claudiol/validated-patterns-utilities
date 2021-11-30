#!/bin/bash

# The INSTALLPATH variable is meant to separate the oc version by path so multiple versions
# can be used on the same host. The INSTALLDIR path is extending INSTALLPATH and mapping towards
# the Cloud Service Provider (CSP) and Region. 


OC_VERSION=4.8.18
CSP=aws
REGION=commercial
INSTALLPATH="" #Example: /home/user1/ocp/${OC_VERSION}
INSTALLDIR=${INSTALLPATH}/${CSP}${REGION}

deploy() {

pushd ${INSTALLPATH}

if [[ -e ./${CSP}${REGION}/install-config.yaml ]]; then
  echo "Install Config exists in ${INSTALLDIR}"
  select ANS in yes no quit ;
  do
    case $ANS in
      yes)
        echo "overwriting existing file"
        cp ./backup/install-config.yaml ${CSP}${REGION}/install-config.yaml
        echo "Running openshift-installer"
        ./openshift-install create cluster --dir=${INSTALLDIR} --log-level=debug
        break
        ;;
      no)
        echo "using existing file"
        echo "Running openshift-installer"
        ./openshift-install create cluster --dir=${INSTALLDIR} --log-level=debug
        break
        ;;
      quit)
        exit 0
        ;;
    esac
 done
  else
   echo "Copying install-config to ${INSTALLDIR}"
   cp ./backup/install-config.yaml ${CSP}${REGION}/install-config.yaml
   echo "Running openshift-installer"
   ./openshift-install create cluster --dir=${INSTALLDIR} --log-level=debug
fi

echo "Install Complete"
}

destroy() {
 pushd ${INSTALLPATH}

 echo "Are you sure you want to destroy the cluster?"
  select ANS in yes no quit ;
  do
    case $ANS in
      yes)
        echo "tearing cluster down"
        ./openshift-install destroy cluster --dir ${CSP}${REGION}/ --log-level=debug
        echo "Cluster destroyed!"
        break
        ;;
      no)
        echo "exiting destroyer"
        break
        ;;
      quit)
        exit 0
        ;;
    esac
 done

}

kube-passwd() {

cat ${INSTALLDIR}/auth/kubeadmin-password | awk -NF'[' '{print $1}'

export KUBECONFIG=${INSTALLDIR}/auth/kubeconfig
echo
echo "URL to the openshift-console"
oc whoami --show-console
echo
echo "API URL"
oc whoami --show-server

}

nodestatus() {
echo "What filters should be used?"
read ANS

exec /usr/local/bin/status-instances.py -f *$ANS*
}

startNodes() {
echo "What filters should be used?"
read ANS

exec /usr/local/bin/start-instances.py -f *$ANS*
}

stopNodes() {
echo "What filters should be used?"
read ANS

exec /usr/local/bin/stop-instances.py -f *$ANS*

}

select ACTION in deploy destroy nodeStatus startNodes stopNodes kube-passwd ;
do 
  case $ACTION in
    deploy)
      deploy
      break
      ;;
    destroy)
      destroy
      break
      ;;
    nodeStatus)
      nodestatus
      break
      ;;
    startNodes)
      startNodes
      break
      ;;
    stopNodes)
      stopNodes
      break
      ;;
    kube-passwd)
      kube-passwd
      break
      ;;
    quit)
      exit 0
      ;;
  esac
done 
