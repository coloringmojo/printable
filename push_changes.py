import subprocess

# --- CONFIG ---
GIT_REMOTE = "origin"     # remote name
GIT_BRANCH = "main"       # branch to push
COMMIT_MESSAGE = "Auto update: layouts, CSS, and generated posts"

# --- ADD ALL CHANGES ---
print("Adding changes...")
subprocess.run(["git", "add", "_layouts/*", "css/*", "_posts/*"])

# --- COMMIT ---
print(f"Committing changes with message: '{COMMIT_MESSAGE}'")
subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE])

# --- PUSH ---
print(f"Pushing to {GIT_REMOTE}/{GIT_BRANCH} ...")
subprocess.run(["git", "push", GIT_REMOTE, GIT_BRANCH])

print("✅ All changes committed and pushed to GitHub!")
