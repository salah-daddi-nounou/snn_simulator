#!/bin/bash

# Function to push the project to timald03
push_to_timald03() {
    sftp timald03 <<EOF
    put -r /home/daddinos/programming/python_projects/snn_simulator /home/users/daddinos/projet_cmos28fdsoi_12/
    bye
EOF
}

# Function to pull the project from timald03
pull_from_timald03() {
    sftp timald03 <<EOF
    get -r /home/users/daddinos/projet_cmos28fdsoi_12/snn_simulator /home/daddinos/programming/python_projects/
    bye
EOF
}

# Main script starts here
if [ $# -ne 1 ]; then
    echo "Usage: $0 <push_to_timald03|pull_from_timald03>"
    exit 1
fi

case $1 in
    push_to_timald03)
        push_to_timald03
        ;;
    pull_from_timald03)
        pull_from_timald03
        ;;
    *)
        echo "Invalid argument. Usage: $0 <push_to_timald03|pull_from_timald03>"
        exit 1
        ;;
esac
