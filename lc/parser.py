# copy problem information from "https://leetcode.com/problemset/all/"
# and then parse it, with "id:name" format
import sys
i = 0
lines = list(sys.stdin)
for i,line in enumerate(lines):
    line=line.strip()
    if line.isdigit():
        name = lines[i+1].strip().split("    ")[0]
        name = name.replace(' ','-').replace('(','').replace(')','')
        name = name.lower()
        print(f"{int(line)} : \"{name}\",")