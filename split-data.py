import os
import shutil
import splitfolders

source_root = r"export\data"
merged_root = r"merged_data"
output_root = r"dataset"

# Create merged class folders
os.makedirs(os.path.join(merged_root, "0"), exist_ok=True)
os.makedirs(os.path.join(merged_root, "1"), exist_ok=True)

# Allowed image extensions
image_exts = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# Go through each numbered folder
for parent_folder in os.listdir(source_root):
    parent_path = os.path.join(source_root, parent_folder)

    if not os.path.isdir(parent_path):
        continue

    for class_label in ["0", "1"]:
        class_path = os.path.join(parent_path, class_label)

        if not os.path.exists(class_path):
            continue

        for file_name in os.listdir(class_path):
            if file_name.lower().endswith(image_exts):
                src_file = os.path.join(class_path, file_name)

                # Add parent folder name to avoid duplicate filenames
                new_name = f"{parent_folder}_{class_label}_{file_name}"
                dst_file = os.path.join(merged_root, class_label, new_name)

                shutil.copy2(src_file, dst_file)

# Split into train / val / test
splitfolders.ratio(
    merged_root,
    output=output_root,
    seed=42,
    ratio=(0.7, 0.15, 0.15)
)

# Rename val -> valid
val_path = os.path.join(output_root, "val")
valid_path = os.path.join(output_root, "valid")

if os.path.exists(val_path):
    os.rename(val_path, valid_path)

print("Done. Standard dataset created successfully.")