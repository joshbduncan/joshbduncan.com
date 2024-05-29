#!/usr/bin/env bash

while read -r image_path; do
  if [[ -f "$image_path" ]]; then
    dimensions=$(identify -format "%w %h" "$image_path")
    width=$(echo "$dimensions" | cut -d ' ' -f 1)
    height=$(echo "$dimensions" | cut -d ' ' -f 2)
    echo "Path: $image_path, width=\"$width\" height=\"$height\""
  else
    echo "File not found: $image_path"
  fi
done
