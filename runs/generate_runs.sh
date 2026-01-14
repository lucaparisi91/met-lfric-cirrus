

MESHDIR=../build_lfric/mesh_scripts/

# Loop over all directories matching pattern CN_M
for dir in "$MESHDIR"/C*_*/; do
    # Check if the directory exists (in case no match is found)
    [ -d "$dir" ] || continue
    
    # Extract directory name without path
    dirname=$(basename "$dir")
    
    # Extract N and M from CN_M pattern
    if [[ $dirname =~ ^C([0-9]+)_([0-9]+)$ ]]; then
        N="${BASH_REMATCH[1]}"
        M="${BASH_REMATCH[2]}"
        echo "N=$N, M=$M"
    fi

    mkdir $dirname


done






