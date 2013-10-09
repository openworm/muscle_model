#compile the pyramidal library:
g++ -c pyramidal.cpp -I /usr/include/python2.7/ -I ./ -l python2.7 -o pyramidal.o
g++ -c example.cpp -I /usr/include/python2.7/ -I ./ -l python2.7 -o example.o

#make an executable:
g++ example.cpp -I /usr/include/python2.7/ -I ./ -l python2.7 -o sim pyramidal.o


