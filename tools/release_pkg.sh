#!/bin/bash

# This shell script is used for build and publish package to PyPI.
# note: Username/password is required to login PyPI server.
#
# usage:
#
# release_pkg.sh v1.0.0 testpypi            # release v1.0.0 to testpypi
#
# release_pkg.sh v1.0.0 pypi                # release v1.1.1 to pypi
#

set -e


PKG_DISTRIBUTE_NAME=alipai
PKG_IMPORT_NAME=pai

version_tag=${1}
repo=${2:-testpypi}

if [[ version_tag != v* ]]; then
  echo "release version tag should be startswith v" && exit 1
fi

pkg_version=${version_tag#v*}

# checkout current git HEAD to specific version tag.
function checkout_release_version() {

  git fetch origin refs/tags/"$version_tag"
  git checkout tags/"$version_tag"

  expected_version=$pkg_version
  current_version=$(cat $PKG_IMPORT_NAME/VERSION)

  # shellcheck disable=SC2053
  if [[ $expected_version != $current_version ]]; then
    echo "expected version is $expected_version, but the current version from file is $current_version" && exit 1
  fi
}

# build and publish the package to PyPI.
function build_and_publish() {
  index_repo=$1
  # install build/publish tools
  python3 -m pip install --upgrade setuptools
  python3 -m pip install wheel
  python3 -m pip install twine

  python3 setup.py clean --all && python3 setup.py bdist_wheel --universal
  wheel_pkg="dist/$PKG_DISTRIBUTE_NAME-$pkg_version-py2.py3-none-any.whl"

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
  else
    echo "unknown PyPI repository."
  fi
}

function main() {
  if [ -z $version_tag ]; then
    echo "please specific the version " && exit 1
  fi

  pkg_root_dir="$(dirname "$0")/.."
  cd "$pkg_root_dir" || (echo "cd the workdir $(pkg_root_dir) fail" && exit 1)

  checkout_release_version $version_tag
  build_and_publish $repo

}

main
