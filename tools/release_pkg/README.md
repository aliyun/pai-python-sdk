# PAI Python SDK Release Package

Tools used to build and publish PAI Python SDK package **<https://code.alibaba-inc.com/PAI/pai-python-sdk/tree/master>** to the OSS bucket **oss://pai-sdk**.

***Visit Aone pipeline to use the tools: <https://cd.aone.alibaba-inc.com/ec/pipelines/55584>***

Specify a git branch name `$BRANCH` to build and release the PAI Python SDK package to the OSS bucket **oss://pai-sdk**. If build success, the package will be packed as **alipai-\${pkg_version}-py2.py3-none-any.whl** and be pushed to **<https://pai-sdk.oss-cn-shanghai.aliyuncs.com/alipai/dist/alipai-${pkg_version}-py2.py3-none-any.whl>**. It will also update the **index.html** which keeps track of all the published package. Visit **<https://pai-sdk.oss-cn-shanghai.aliyuncs.com/repo/index.html>** to check all the published versions of PAI Python SDK.

## usage:
### Dockerfile:

Build a docker image that contains all the environments that the shell script `release_pkg_to_oss.sh` need.  

This docker image does not have any editor within it. To use the shell script, it is suggested that either install an editor or mount the docker with a local directory which contains the script.

```bash
# e.g.	build a docker image called test_dockerfile with tag 1.0 
#		and run a container that is mounted with a local directory:
$docker build -t test_dockerfile:1.0 - < Dockerfile
$docker run -it -v /directory/contains/script:/work/directory test_dockerfile:1.0 /bin/bash
```

### release_pkg_to_oss.sh:  
Specify a git branch name `$BRANCH` to build and publish the package to OSS bucket. OSS config and git config are required.  

git branch name `$BRANCH`, OSS username `$OSS_ACCESS_KEY_ID`, OSS password `$OSS_ACCESS_KEY_SECRET`, git username `$GIT_USERNAME` and git private token `$GIT_PRIVATE_TOKEN` are needed to be passed as enviornment variables to use the script.  

```bash
# e.g.	run the shell script:
./release_pkg_to_oss.sh			# release specific branch to OSS bucket
								# need to specify $BRANCH, $OSS_ACCESS_KEY_ID, $OSS_ACCESS_KEY_SECRET, $GIT_USERNAME and $GIT_PRIVATE_TOKEN
```

### repo/index.html
If build and publish succeed, the shell script will also update the **index.html** which keeps track of all the published PAI Python SDK packages.

Visit **<https://pai-sdk.oss-cn-shanghai.aliyuncs.com/repo/index.html>** to check all the published versions of PAI Python SDK.
