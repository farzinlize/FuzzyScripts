
# inside /usr/lib/[python]/venv (for example use python3.12)
# bottom of main function usually inside __init__.py file
# add these line in main function of venv module to make easy symlink -> <env-name>/activate instead of <env-name>/bin/activate
print("[FARZIN-HACK] [make symlink for activate] [inside /usr/lib/python3.12/venv]")
if options.dirs:os.symlink(f"bin/activate", f"{options.dirs[0]}/activate")
# I used it for python3.10 and python3.12 (here is 3.12)
