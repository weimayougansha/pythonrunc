import os
import shutil
import pdb


def init_fs(root_path, volume):
    # pdb.set_trace()
    os.system("mount --bind %s %s" % (root_path, root_path))
    root_path = add_persistent_volume(root_path, volume)
    pivot_root_path = os.path.join(root_path, ".pivot_root")
    if not os.path.isdir(pivot_root_path):
        os.makedirs(pivot_root_path)
    os.system("pivot_root %s %s" % (root_path, pivot_root_path))
    os.chdir("/")
    os.system("umount -l /.pivot_root")
    os.rmdir("/.pivot_root")
    # mount proc
    os.system("mount -t proc proc /proc")
    # mount tmpfs
    os.system("mount -t tmpfs devtmpfs /dev")
    # mount null
    os.system("mknod /dev/null c 1 3")


def get_overlayfs_from_file(tar_path, container_id):
    # merge_layer = lowwer_layer + upper_layer
    tar_parent_dir_path = os.path.dirname(tar_path)
    lowwer_layer_name = "lowwer_layer_" + container_id
    lowwer_layer_path = get_read_only_layer(tar_path, tar_parent_dir_path, lowwer_layer_name)
    upper_layer_name = "upper_layer_" + container_id
    upper_layer_path = get_layer_path(tar_parent_dir_path, upper_layer_name)
    merge_layer_name = "merge_layer_" + container_id
    merge_lay_path = get_layer_path(tar_parent_dir_path, merge_layer_name)
    work_layer_name = "work_layer_" + container_id
    work_lay_path = get_layer_path(tar_parent_dir_path, work_layer_name)
    merge_result = os.system("mount -t overlay overlay -o lowerdir=%s,upperdir=%s,workdir=%s %s"
              % (lowwer_layer_path, upper_layer_path, work_lay_path, merge_lay_path)
              )
    return merge_lay_path if merge_result == 0 else None


def get_read_only_layer(tar_path, tar_parent_dir_path, lowwer_layer_name):
    lowwer_layer_path = os.path.join(tar_parent_dir_path, lowwer_layer_name)
    if os.path.isdir(lowwer_layer_path):
        shutil.rmtree(lowwer_layer_path)
    os.mkdir(lowwer_layer_path)
    tar_result = os.system("tar -xf %s -C %s" % (tar_path, lowwer_layer_path))
    if tar_result == 0:
        return lowwer_layer_path
    else:
        return None


def get_layer_path(tar_parent_dir_path, layer_name):
    layer_path = os.path.join(tar_parent_dir_path, layer_name)
    if os.path.isdir(layer_path):
       shutil.rmtree(layer_path)
    os.mkdir(layer_path)
    return layer_path


def add_persistent_volume(root_path, volume_path):
    if volume_path == None:
        return root_path
    local_volume_path, mount_volume = volume_path.split(":")
    mount_volume_path = (root_path + mount_volume[1:]) if root_path.endswith('/') else (root_path + mount_volume)
    os.system("mount --bind %s %s" % (local_volume_path, mount_volume_path))
    return root_path


def rm_fs(tar_path, container_id):
    tar_parent_dir_path = os.path.dirname(tar_path)
    for layer_name in ["lowwer_layer", "upper_layer", "merge_layer", "work_layer"]:
        layer_name = layer_name + '_' + container_id
        layer_path = os.path.join(tar_parent_dir_path, layer_name)
        if os.path.isdir(layer_path):
            shutil.rmtree(layer_path)










