#!/usr/bin/env python3
import os
import argparse
import sys

def find_context_files(start_path):
    """Find .context.md files and GEMINI.md from start_path up to root."""
    files = []
    current = os.path.abspath(start_path)
    if not os.path.exists(current):
        print(f"Error: Path {current} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    if os.path.isfile(current):
        current = os.path.dirname(current)
        
    # Get project root (assumed to be the directory containing .git or GEMINI.md)
    project_root = None
    temp = current
    while temp != "/":
        if os.path.isfile(os.path.join(temp, "GEMINI.md")):
            project_root = temp
            # Don't break yet, we might want to go higher if there are nested projects, 
            # but for this NAS project, the first GEMINI.md usually marks the root.
            break
        temp = os.path.dirname(temp)
    
    if not project_root:
        project_root = "/" # Fallback
        
    temp = current
    while True:
        # Check for .context.md
        ctx_file = os.path.join(temp, ".context.md")
        if os.path.isfile(ctx_file):
            files.append(ctx_file)
            
        # Check for GEMINI.md at root
        gemini_file = os.path.join(temp, "GEMINI.md")
        if os.path.isfile(gemini_file):
            files.append(gemini_file)
            
        if temp == project_root or temp == "/":
            break
        temp = os.path.dirname(temp)
        
    return files

def get_overlay_path(project_root, task_name):
    """Resolve a task/role overlay path."""
    overlay_path = os.path.join(project_root, ".context", f"{task_name}.md")
    if os.path.isfile(overlay_path):
        return overlay_path
    return None

def merge_context(files, overlay=None):
    """Merge context files into a single string with attribution."""
    merged = []
    
    # Priority: Nearest first. The find_context_files returns them in nearest-to-root order.
    for f in files:
        with open(f, 'r') as content_file:
            merged.append(f"<!-- Source: {f} -->\n{content_file.read()}\n")
            
    if overlay:
        with open(overlay, 'r') as content_file:
            # Overlays are usually high priority or appended
            merged.insert(0, f"<!-- Source: {overlay} (Role Overlay) -->\n{content_file.read()}\n")
            
    return "\n---\n\n".join(merged)

def main():
    parser = argparse.ArgumentParser(description="Aggregate project context based on path and task.")
    parser.add_argument("--path", default=".", help="Directory to start context resolution from.")
    parser.add_argument("--task", help="Role or task overlay to include (e.g., 'security').")
    
    args = parser.parse_args()
    
    context_files = find_context_files(args.path)
    
    # Find project root for overlays
    project_root = None
    for f in context_files:
        if os.path.basename(f) == "GEMINI.md":
            project_root = os.path.dirname(f)
            break
    
    overlay_file = None
    if args.task and project_root:
        overlay_file = get_overlay_path(project_root, args.task)
        if not overlay_file:
            print(f"Warning: Overlay '{args.task}' not found in {project_root}/.context/", file=sys.stderr)
            
    print(merge_context(context_files, overlay_file))

if __name__ == "__main__":
    main()
