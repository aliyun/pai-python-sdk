#!/bin/bash

#To use the script, you must have ossutil in your system PATH and config the client tool to visit the "pai-sdk" OSS bucket.
#
#usage:
#
# publish_doc preview              # publish preview documents
# publish_doc production           # publish production documents
#

set -e

function cd_docs_dir() {
  docs_dir="$(dirname "$0")/../docs"
  cd "$docs_dir" || (echo "cd the workdir $(docs_dir) fail" && exit)
}

function build_doc() {
  nox -s doc
}

function publish_preview_doc() {
  build_doc
  public_doc preview/doc/html
  echo "please visit link https://pai-sdk.oss-cn-shanghai.aliyuncs.com/pai/preview/doc/html/index.html to view the documents."
}

function public_production_doc() {
  build_doc
  public_doc doc/html
  echo "please visit link https://pai-sdk.oss-cn-shanghai.aliyuncs.com/pai/doc/html/index.html to view the documents."
}
#
function public_doc() {
  if [ -z "$1" ]; then
    echo "target_path not exists" && exit 1
  fi
  echo "target_path is $1"

  ossutilmac64 cp build/html oss://pai-sdk/pai/"$1" --recursive -f
}

release_type=${1:-preview}

if [ $release_type == "preview" ]; then
  publish_preview_doc
elif [ $release_type == "production" ]; then
  public_production_doc
else
  echo "unknown release_type: $release_type" && exit 1
fi
