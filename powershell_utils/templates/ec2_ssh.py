"""EC2 SSH template for powershell."""
from os import PathLike
from pathlib import Path


def get_ec2_ssh_fns(
    instance_name: str,
    instance_id: str, 
    pemfile_path: PathLike = None,
    username: str = "ec2-user",
):
    """Yield string values for ec2 ssh functions."""
    pemfile_str = f" -i {pemfile_path}" if pemfile_path else ""
    command_names = [ 
        f"Get{instance_name}Ip",
        f"Start{instance_name}",
        f"Stop{instance_name}",
        f"SSH{instance_name}",
    ]
    cmd_str = f"\
    function {command_names[0]} {{\
        aws ec2 describe-instances --instance-ids {instance_id} --query 'Reservations[0].Instances[0].PublicIpAddress' --output text\
    }}\
    function {command_names[1]} {{\
        aws ec2 start-instances --instance-ids {instance_id}\
    }}\
    function {command_names[2]} {{\
        aws ec2 stop-instances --instance-ids {instance_id}\
    }}\
    function {command_names[3]} {{\
        ssh {pemfile_str} {username}@{{Get{instance_name}Ip}}\
    }}"
    return cmd_str, command_names 
    


