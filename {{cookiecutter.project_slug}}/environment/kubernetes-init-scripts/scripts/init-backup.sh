#!/bin/bash

source ./scripts/defaults.sh

cat << EOF
apiVersion: v1
data:
    SLACK_URL: `echo -n $BACKUP_SLACK_URL | base64 -w 0`
    GCE_ACCOUNT: `echo -n $BACKUP_GCE_ACCOUNT | base64 -w 0`
    GCE_BUCKET: `echo -n $BACKUP_GCE_BUCKET | base64 -w 0`
    GCE_KEY: `echo -n $BACKUP_GCE_KEY | base64 -w 0`
kind: Secret
metadata:
  name: {{cookiecutter.project_slug_dashed}}-backend-$TIER-aidbox-backup
  namespace: {{cookiecutter.cluster_name_prefix}}-backend-$TIER
type: Opaque
EOF
