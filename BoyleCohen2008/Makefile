# Must indent with "tab" *not* spaces (damn!)
#

TARGET=program

CXX=g++ -O3
CC=$(CXX)
SRCS=$(shell ls *.cc)
OBJS=$(subst .cc,.o,$(SRCS))

$(TARGET): $(OBJS)
	$(CXX) $(OBJS) -o $(TARGET)

check:
	@echo SRCS = $(SRCS)
	@echo OBJS = $(OBJS)

clean:
	rm -rf $(TARGET) $(OBJS)

depend:
	$(CXX) -MM $(SRCS) > .depends.mk

-include .depends.mk
