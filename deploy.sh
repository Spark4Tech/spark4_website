#!/bin/bash
# Sync only the images directory
rsync -avz -e "ssh -i ~/.ssh/AWS.pem" \
    app/static/images/ \
    ubuntu@ec2-54-244-100-42.us-west-2.compute.amazonaws.com:~/spark4/app/static/images/

rsync -avz -e "ssh -i ~/.ssh/AWS.pem" \
    app/static/blog/images/ \
    ubuntu@ec2-54-244-100-42.us-west-2.compute.amazonaws.com:~/spark4/app/static/blog/images/