

class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.data = {}

    def has_key(self, name):  # variable name
        return name in self.data

    def get(self, name):         # get from memory current value of variable <name>
        return self.data[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.data[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.memories = []
        self.memories.append(memory) if memory is not None

    def get(self, name):             # get from memory stack current value of variable <name>
        for memory in reversed(memories):
            if memory.has_key(name):
                return memory.get(name)
        return None

    def put(self, name, value): # puts into memory stack current value of variable <name>
        self.memories[-1].put(name, value)

    def push(self, memory): # push memory <memory> onto the stack
        self.memories.append(memory)

    def pop(self):          # pops the top memory from the stack
        self.memories.pop()


