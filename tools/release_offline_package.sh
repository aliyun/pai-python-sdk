#!/bin/bash

# This shell script is used for build and publish offline package.
# Note: ossutil client tool and OSS config for ossutil is required to upload package to OSS bucket.

set -e

function help() {
  echo "
usage:

release_offline_package.sh                                # build and check package with default image(Python:3.7).
release_offline_package.sh -i python:3.8                  # build and check package with image Python:3.8.
release_offline_package.sh -i python:3.7 -p true          # build and release package to OSS.
"
  exit 0

}


image_uri=python:3.7
publish=''


while getopts 'i:p:h:' OPT; do
    case $OPT in
        i) image_uri="$OPTARG";;
        p) publish="$OPTARG";;
        h) help;;
        ?) help;;
    esac
done

echo "Build package with image_uri: $image_uri, publish: $publish"


PKG_DISTRIBUTE_NAME=alipai
PKG_IMPORT_NAME=pai

pkg_root_dir="$(dirname "$0")/.."
release_version=$(cat $pkg_root_dir/$PKG_IMPORT_NAME/VERSION)

env_name=`echo "$image_uri" | tr ":" -`
fat_package_name="alipai-$release_version-$env_name.tag.gz"


function check() {
  docker run --rm --network none -w /root -v $(pwd)/dist:/tmp python:3.7 \
    bash -ec "tar -C /root -xzvf /tmp/$fat_package_name && \
   python -m pip install --no-index --find-links /root/wheels /root/wheels/alipai*.whl && \
   python -c 'import pai; print(pai.__version__)'"

}

function build_fat_package() {
  docker run --rm -w /root --env PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ -v $(pwd)/:/root python:3.7 \
    bash -ec "python -m pip install --upgrade pip && rm -rf ./wheels && \
    python -m pip wheel . -w ./wheels && \
     tar -czvf ./dist/$fat_package_name ./wheels/"
}

function publish() {
  echo "Begin publish package to OSS"
  sleep 3
  fat_package_path="dist/$fat_package_name"
  ossutilmac64 cp dist/$fat_package_name oss://pai-sdk/$PKG_DISTRIBUTE_NAME/dist/
  echo "succeed upload offline-install package to OSS."
  echo "https://pai-sdk.oss-cn-shanghai.aliyuncs.com/$PKG_DISTRIBUTE_NAME/dist/$fat_package_name"

}

function main() {
  cd "$pkg_root_dir" || (echo "cd the workdir $(pkg_root_dir) fail" && exit 1)
  build_fat_package
  check
  if [ $publish ]; then
    publish
  fi
}

main
