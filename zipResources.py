
import os
import shutil

print ("Python running...")

print ("Grabbing datapack directories...")
subfolders = [ f.name for f in os.scandir("src/res/") if f.is_dir() ]
for folder in subfolders:
    print ("\tZipping datapack '{}'".format(folder))
    shutil.make_archive("dist/res/{}".format(folder), 'zip', 'src/res/{}'.format(folder))
print ("Python completed.")
