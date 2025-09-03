#!/usr/bin/env python3
import sys
import pathlib
import re
import yaml

RULE_DIR = pathlib.Path(".cursor/rules")
REQUIRED = {
    "enterprise_mode.mdc": {"alwaysApply": False, "forbid_globs": True},
    "free_mode.mdc": {"alwaysApply": False, "forbid_globs": True},
    "mcp_server_usage.mdc": {"alwaysApply": True, "forbid_globs": False},
}

def read_front_matter(text):
    # More flexible regex to handle various front matter formats
    # Handle files that might start with whitespace/newlines
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        # Try alternative format without trailing newline
        m = re.match(r"^\s*---\s*\n(.*?)\n---", text, re.S)
    if not m:
        raise ValueError("Missing YAML front matter")
    return yaml.safe_load(m.group(1))

def main():
    if not RULE_DIR.exists():
        print("FAIL: .cursor/rules/ missing")
        sys.exit(2)

    errors = []
    for name, req in REQUIRED.items():
        p = RULE_DIR / name
        if not p.exists():
            errors.append(f"Missing rule file: {name}")
            continue
        
        try:
            fm = read_front_matter(p.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{name}: invalid front matter - {e}")
            continue
            
        # 1) Must NOT contain `type`
        if "type" in fm:
            errors.append(f"{name}: remove 'type' from front matter")
        
        # 2) alwaysApply matches
        if bool(fm.get("alwaysApply", False)) != req["alwaysApply"]:
            errors.append(f"{name}: alwaysApply should be {req['alwaysApply']}")
        
        # 3) globs rules
        has_globs = "globs" in fm and bool(fm["globs"])
        if req["forbid_globs"] and has_globs:
            errors.append(f"{name}: must NOT have globs for Agent Requested")
        if not req["forbid_globs"] and fm.get("alwaysApply") and has_globs:
            errors.append(f"{name}: Always rules should not need globs")
        
        # 4) description required
        if not fm.get("description") or not str(fm["description"]).strip():
            errors.append(f"{name}: missing non-empty description")

    if errors:
        print("FAIL:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    
    print("OK: Cursor rules verified")
    sys.exit(0)

if __name__ == "__main__":
    main()
