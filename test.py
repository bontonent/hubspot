import re

print(int(re.match(r"You are currently on Page (\d)","You are currently on Page ").group(1)))

