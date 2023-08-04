#!/bin/bash

# This shell script is used to build and publish PAI Python SDK package to OSS.
# note: Specify a branch name($BRANCH) to build and publish package to OSS.
#		OSS config and git config are required to upload the package to OSS bucket.
#		git branch name($BRANCH), OSS username ($OSS_ACCESS_KEY_ID), OSS password ($OSS_ACCESS_KEY_SECRET),
#		git username ($GIT_USERNAME) and git private token($GIT_PRIVATE_TOKEN) are needed to be
#		passed as environment variables to use the script.
#
# usage:
#
# ./release_pkg_to_oss.sh                        # release specific branch to OSS.


BUCKET="pai-sdk"
PKG_DISTRIBUTE_NAME=alipai
PKG_IMPORT_NAME=pai
DIR_NAME=pai-python-sdk

# BRANCH=""
# OSS_ACCESS_KEY_ID=""
# OSS_ACCESS_KEY_SECRET=""
# GIT_USERNAME=""
# GIT_PRIVATE_TOKEN=""

version_tag=""
pkg_version=""

ossutil config -e https://oss-cn-shanghai.aliyuncs.com -i ${OSS_ACCESS_KEY_ID} -k ${OSS_ACCESS_KEY_SECRET} -L EN
ossutil cp oss://$BUCKET/repo/index.html "./" -u


# check branch and version before build
function check(){
	# pulling git package
	echo -e "Pulling the latest PAI Python SDK package:"
	if [ -d $DIR_NAME ];then
	    (cd $DIR_NAME/ && git pull origin)
	    (cd $DIR_NAME/ && git fetch origin)
	else
	    git clone http://${GIT_USERNAME}:${GIT_PRIVATE_TOKEN}@gitlab.alibaba-inc.com/PAI/pai-python-sdk.git
	fi
	[ -d $DIR_NAME ] || (echo -e "\nERROR: git clone failed, pai-python-sdk not found." && exit 1)
	echo -e "Succeed: PAI Python SDK package cloned at './$DIR_NAME'\n"


	# checking branch
	echo -e "Branch check:"
	BRANCH_list=$(cd $DIR_NAME/ && git branch -lr)
	BRANCH_str="origin/$BRANCH"
	result=$(echo "$BRANCH_list" | grep -x "\s\+\\${BRANCH_str}")
	if [[ $BRANCH_str == "origin/" ]];then
		echo -e "\nERROR: release branch not specified; build failed" && exit 1
	elif [[ $result == "" ]];then
	    echo -e "\nERROR: branch '$BRANCH_str' does not exist; build failed" && exit 1
	else
		echo -e "Succeed: branch check success; switching to branch '$BRANCH_str'"
		(cd $DIR_NAME/ && git checkout . && git switch $BRANCH)
	fi


	# checking version tag and git tag
	echo -e "\nGit Tag/Version check:"
	version_tag=$(cat $DIR_NAME/$PKG_IMPORT_NAME/VERSION)
	pkg_version=${version_tag#v*}
	tag_list=$(cd $DIR_NAME/ && git tag -l)
	tag_str=$version_tag
	result=$(echo "$tag_list" | grep -x "${tag_str}")
	if [[ $result != "" ]];then
	    echo -e "\nERROR: git tag '$tag_str' already exist in git repo; build failed" && exit 1
	fi

	version_list=$(cat index.html)
	version_str="$PKG_DISTRIBUTE_NAME-$pkg_version-py2.py3-none-any.whl"
	result=$(echo "$version_list" | grep -x "${version_str}")
	if [[ $result != "" ]];then
	    echo -e "\nERROR: version '$version_str' already exist in index.html; build failed" && exit 1
	fi

	echo -e "Succeed: git tag/version check success; SDK package '$version_str' will be built and published to OSS '$BUCKET/$PKG_DISTRIBUTE_NAME/dist'"
	(cd $DIR_NAME/ && git tag $version_tag)
	(cd $DIR_NAME/ && git push origin $version_tag)
	echo -e "\n"
}


# build and publish the package to OSS.
function build_and_publish_to_oss() {
	# install build/publish tools
	python3 -m pip install --upgrade setuptools
	python3 -m pip install wheel
	python3 -m pip install twine

	echo -e "Building and publishing package '$wheel_pkg' to OSS bucket '$BUCKET/$PKG_DISTRIBUTE_NAME/dist/'"
	(cd pai-python-sdk && python3 setup.py clean --all && python3 setup.py bdist_wheel --universal)
	wheel_pkg="$DIR_NAME/dist/$PKG_DISTRIBUTE_NAME-$pkg_version-py2.py3-none-any.whl"

	[ -f "$wheel_pkg" ] || ( echo -e "\nERROR: build failed. wheel package '$wheel_pkg' not found." && exit 1)
	python3 -m twine check "$wheel_pkg" || (echo -e "\nERROR: twine check failed" && exit 1)

	ossutil cp "$wheel_pkg" oss://$BUCKET/$PKG_DISTRIBUTE_NAME/dist/ -u
	echo -e "Succeed: upload success; package has been pushed to oss bucket '$BUCKET/$PKG_DISTRIBUTE_NAME/dist/', please visit:"
	echo -e "https://$BUCKET.oss-cn-shanghai.aliyuncs.com/$PKG_DISTRIBUTE_NAME/dist/$PKG_DISTRIBUTE_NAME-$pkg_version-py2.py3-none-any.whl\n"

	echo -e "Updating the repo html"
	ossutil cp oss://$BUCKET/repo/index.html "./" -u
	new_index="<a href=\"https://$BUCKET.oss-cn-shanghai.aliyuncs.com/$PKG_DISTRIBUTE_NAME/dist/$PKG_DISTRIBUTE_NAME-$pkg_version-py2.py3-none-any.whl\">\n\
$PKG_DISTRIBUTE_NAME-$pkg_version-py2.py3-none-any.whl\n\
</a><br>"
	sed -i "12 a\\$new_index" index.html
	ossutil cp index.html oss://$BUCKET/repo/  -u
	echo -e "Succeed: update success. repo index has been updated, please visit:"
	echo -e "https://$BUCKET.oss-cn-shanghai.aliyuncs.com/repo/index.html\n"
}


function main() {
	# pkg_root_dir="/yutou/pai_python_sdk_cicd_test"
	# cd "$pkg_root_dir" || (echo -e "\nERROR: cd the workdir $(pkg_root_dir) failed" && exit 1)

	check
	build_and_publish_to_oss
}


main
