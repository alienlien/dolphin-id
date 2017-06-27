#!/bin/bash
# This script installs bazel and OpenJDK 1.8 for ubuntu 14.04
# Ref: https://gist.github.com/arundasan91/468bec87efa6ea7abdff59a30b43d140
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get update && sudo apt-get -y install openjdk-8-jdk
echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get -y install bazel
# sudo apt-get upgrade bazel
