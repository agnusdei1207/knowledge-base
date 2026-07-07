import os
import re

# Subject 1 (026-050) frontmatter fix
directory_1 = "/home/user/study/content/cspe/01_basic_theory/"
files_to_fix = [
    "026_twos_complement.md", "027_logic_gates_boolean.md", "028_combinational_logic.md",
    "029_sequential_logic.md", "030_hamming_code.md", "031_information_theory.md",
    "032_huffman_coding.md", "033_run_length_encoding.md", "034_source_vs_channel_coding.md",
    "035_matrix_operations.md", "036_linear_transformation.md", "037_eigenvalue_eigenvector.md",
    "038_bayes_theorem.md", "039_probability_distribution.md", "040_hypothesis_testing.md",
    "041_regression_analysis.md", "042_clustering.md", "043_pca.md", "044_similarity_measures.md",
    "045_k_fold_cv.md", "046_overfitting_bias_variance.md", "047_activation_functions.md",
    "048_backpropagation.md", "049_gradient_descent.md", "050_loss_functions.md"
]

for filename in files_to_fix:
    filepath = os.path.join(directory_1, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if lines[0].startswith("---"):
        print(f"Skipping {filename}, already has frontmatter.")
        continue
    
    # Extract title from the first line (# NNN. Title...)
    title_line = lines[0].strip()
    match = re.match(r"# \d{3}\. (.*) \[출제:.*\]", title_line)
    if match:
        title_val = match.group(1).strip()
    else:
        title_val = title_line.lstrip("# ").strip()
    
    weight_match = re.match(r"# (\d{3})\.", title_line)
    weight_val = int(weight_match.group(1)) if weight_match else 0
    
    frontmatter = f"""---
title: "{title_val}"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: {weight_val}
---

"""
    # Replace first line with frontmatter and the title line again if needed, 
    # but the subagent's content already has the title line as line 1.
    # So we just prepend the frontmatter.
    new_content = frontmatter + "".join(lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed frontmatter for {filename}")

# Remove duplicate directories
os.system("rm -rf /home/user/study/content/docs/compu/")
os.system("rm -rf /home/user/study/content/posts/cspe/")
print("Removed legacy directories docs/compu and posts/cspe")
