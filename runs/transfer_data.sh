#!/bin/bash

# Transfer gungho runs data from z04 before it gets deleted
# Run analysis on the field for large datasets

src_dir=/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/runs # Source directory
dst_dir=. # Destination directory
dry_run=false
action="copy"

target_directory_pattern="nodes192*pat_*"



# Find all directories of pattern *sampling* in the source directory and copy them to the destination directory
find $src_dir -maxdepth 1 -type d -name "$target_directory_pattern" | while read dir; do
    #echo ": $dir to $dst_dir"
    #rsync --info=progress2 -r "$dir" "$dst_dir"
    
    out_dir="$dst_dir/$(basename $dir)"
    
    cmd="cp $dir/report.txt $out_dir"

     echo "[echo] mkdir -p $out_dir"
    echo "[echo] $cmd"

    # Execute command or print it if dry run
    if [ "$dry_run" = true ]; then
       

        continue
    else
        mkdir -p "$out_dir"
        eval "$cmd"
    fi

done