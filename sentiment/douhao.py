#fi = open('edges.txt', 'r')
fi = open('g2geo.txt', 'r')
#fo = open('edges.csv', 'w')
fo = open('g2geo.csv', 'w')

while 1:
    line = fi.readline()
    if not line:
        break
    list = line.split()
    first_item = list.pop(0)
    fo.write(first_item)
    for item in list:
        fo.write(','+str(item))
    fo.write('\n')
