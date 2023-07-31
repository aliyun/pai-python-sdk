#!/bin/bash

# This shell script is used for build and publish package to PyPI/OSS.
# note: username/password is required to login PyPI server while oss config is
# required to upload package to OSS bucket.
#
# usage:
#
# release_pkg.sh testpypi v1.0.0            # release v1.0.0 to testpypi
#
# release_pkg.sh pypi v1.0.2                # release v1.1.1 to pypi
#
# release_pkg.sh oss                        # release local package to OSS.
#

set -e


PKG_DISTRIBUTE_NAME=alipai
PKG_IMPORT_NAME=pai

repo=${1:-testpypi}
version_tag=${2}

if [[ $version_tag != v* && $repo != "oss" ]]; then
  echo "release version tag should be startswith v" && exit 1
fi

pkg_version=${version_tag#v*}

# switch current git HEAD to specific version tag.
function switch_to_release_version() {

  if [ $repo != "oss" ]; then
    git fetch origin refs/tags/"$version_tag"
    git checkout tags/"$version_tag"
  fi

  expected_version=$pkg_version
  current_version=$(python setup.py --version)

  # shellcheck disable=SC2053
  if [[ $expected_version != $current_version ]]; then
    echo "expected version is $expected_version, but the current version from file is $current_version" && exit 1
  fi
}

# build and publish the package to PyPI.
function build_and_publish() {
  index_repo=$1
  pkg_version=$2
  # install build/publish tools
  python3 -m pip install --upgrade setuptools build
  python3 -m pip install twine

  rm -rf dist/ && python3 -m build
  wheel_pkg="dist/$PKG_DISTRIBUTE_NAME-$pkg_version-py3-none-any.whl"

  [ -f "$wheel_pkg" ] || ( echo "build failure, wheel package($wheel_pkg) not found." && exit 1)
  python3 -m twine check "$wheel_pkg" || (echo "twine check failed" && exit 1)

  if [ "$index_repo" == "testpypi" ]; then
    echo "publish package($wheel_pkg) to Test PyPI"
    python3 -m twine upload -r testpypi "$wheel_pkg"
    echo "Succeed upload package to testpypi!"
  elif [ "$index_repo" == "pypi" ]; then
    echo "publish package($wheel_pkg) to Test PyPI"
    python3 -m twine upload -r pypi "$wheel_pkg"
    echo "Succeed upload package to PyPI!"
  elif [ "$index_repo" == "oss" ]; then
    echo "publish package($wheel_pkg) to OSS Bucket"
    ossutilmac64 cp $wheel_pkg oss://pai-sdk/$PKG_DISTRIBUTE_NAME/dist/
    echo "Succeed upload package to OSS, please visit:"
    # Encode the url to avoid the '+' in the url be decoded to ' ' by the browser.
    echo $(echo "https://pai-sdk.oss-cn-shanghai.aliyuncs.com/$PKG_DISTRIBUTE_NAME/$wheel_pkg" | sed 's/+/%2B/g')
  else
    echo "unknown PyPI repository."
  fi
}

function main() {

  pkg_root_dir="$(dirname "$0")/.."
  cd "$pkg_root_dir" || (echo "cd the workdir $(pkg_root_dir) fail" && exit 1)

  if [ $repo != "oss" ]; then
    switch_to_release_version
  fi
  release_version=$(python setup.py --version)
  echo "ReleaseVersion" $release_version

  build_and_publish $repo $release_version

}

main
