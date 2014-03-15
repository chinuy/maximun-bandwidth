import random
import sys

class Heap:

    def __init__(self):
        # array item type: tuple, (id, value)
        self.array = [(0,-1)]

    def getMin(self):
        return self.array[1]

    def insert(self, elm):
        self.array.append(elm)
        i_child = len(self.array) -1
        i_parent = int(i_child/2)
        if i_child > 2: # more than one element
            self.adjust(i_parent, i_child)

    def adjust(self, i_parent, i_child):
        #print self.array, i_parent, i_child
        if self.array[i_parent][1] > self.array[i_child][1]:
            self.swap(i_parent, i_child)
            self.adjust(int(i_parent/2), i_parent)

    def delete_root(self):
        if len(self.array) < 1:
            return

        root_index = 1
        self.array[root_index] = self.array[-1]
        del self.array[-1]
        self.downAdjust(root_index)

    def downAdjust(self, index):
        #print self.array, index
        smaller_index = index*2
        c1 = self.array[index*2][1]
        c2 = sys.maxsize
        if len(self.array) > index*2 +1:
            c2 = self.array[index*2+1][1]
        if c1 > c2:
            smaller_index = index*2 +1

        if self.array[index][1] > self.array[smaller_index][1]:
            self.swap(index, smaller_index)
            self.downAdjust(smaller_index)

    def swap(self, a, b):
        self.array[a], self.array[b] = self.array[b], self.array[a]
        return

def main():

    h = Heap()
    x = range(10)
    random.shuffle(x)
    x = zip(range(5), [1,3,5,8,1])
    for i in range(10):
        h.insert(i)
    h.delete_root()
    print h.array

if __name__ == '__main__':
    main()
