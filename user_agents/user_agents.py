def get_agent(BASE_DIR):
    with open("".join([str(BASE_DIR),'user_agents.txt'])) as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            lines[i] = line.replace('\n','').split('|')[-1].strip()

    return lines

# Example how use
if __name__ =='__main__':
    data = get_agent()
    print(data)