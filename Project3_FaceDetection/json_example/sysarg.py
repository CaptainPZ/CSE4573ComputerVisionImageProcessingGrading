import sys

print("Total lenth of sys.argv is {:3d}".format(len(sys.argv)))

for i, arg in enumerate(sys.argv):
    print("The {} th argument is {}".format(i, arg))
