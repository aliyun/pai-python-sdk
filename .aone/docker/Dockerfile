FROM reg.docker.alibaba-inc.com/alibase/alios7u2-min


## Aone 自定义镜像强依赖，勿删除: start
# Documents: https://yuque.antfin.com/aone/platform/usedocker
# Example: https://code.alibaba-inc.com/cise/docker-image/blob/master/Dockerfile_sample
###########################################################################################################################
# 配置强依赖，勿删除，如需要其他jdk版本，请另行安装，这里不会冲突
RUN yum install -b current -y ajdk git &&\
    rpm -e --noscripts --justdb ajdk &&\
    yum history new &&\
    yum clean all &&\
    rm -rf /var/cache/yum &&\
    mkdir -p /opt/taobao/cise &&\
    mv -f "$(realpath /opt/taobao/java)" /opt/taobao/cise/java &&\
    rm -f /opt/taobao/java &&\
    ln -s /opt/taobao/cise/java/bin/* /usr/local/bin &&\
    echo -e '[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\ntrusted-host = mirrors.aliyun.com' > /etc/pip.conf

# 配置pip并安装pexpect，部分插件依赖了pexpect，不需要的可以删除
RUN yum install -y python-pip &&\
    pip install --no-cache-dir pexpect &&\
    yum clean all &&\
    rm -rf /var/cache/yum

## Aone 自定义镜像强依赖，勿删除: end
###########################################################################################################################


# Install miniconda3 from aliyun mirror:  http://mirrors.aliyun.com/anaconda/miniconda/
ARG MINICONDA_VERSION=Miniconda3-py37_4.12.0
RUN wget http://mirrors.aliyun.com/anaconda/miniconda/${MINICONDA_VERSION}-Linux-x86_64.sh  \
    && bash ${MINICONDA_VERSION}-Linux-x86_64.sh -p /miniconda -b \
    && rm ${MINICONDA_VERSION}-Linux-x86_64.sh

# Miniconda config
ENV PATH=/miniconda/bin:${PATH}
ADD condarc /root/.condarc
RUN conda clean -i
