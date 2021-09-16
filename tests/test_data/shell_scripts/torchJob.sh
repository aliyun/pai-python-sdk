# torchJob.sh
# 使用ScriptOperator operator提交时，会以以下方式执行
# torchJob.sh --epochs {input_param_epochs} --batch_size {input_param_batch_size}

epochs=${2:-10}
batch_size=${4:-32}

cat << EOT > torchJobFile
name=cli_pytorch_job
kind=PyTorchJob
worker_count=3
worker_cpu=10
worker_gpu=1
worker_memory=10
worker_image=master0:5000/minghong/deepops/bert:rdma-pytorch-mnist
workspace_id=wstpgjr5depc3qaw
priority=0
command=export NCCL_IB_DISABLE=1  && /opt/conda/bin/python3 /data/user/ken/demo/mnist-pytorch/mnist.py --backend nccl --epochs=$epochs --batch_size=$batch_size
EOT


#dlc-cli create-job --params_file=torchJobFile

echo "ppochs is $epochs"
echo "batch_size is $batch_size"
