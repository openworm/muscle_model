#ifndef PYRAMIDALSIMULATION_H
#define PYRAMIDALSIMULATION_H

class PyramidalSimulation{

 private: 
  PyObject *pName, *pModule, *pDict, *pFunc, *pValue, *pClass, *pInstance;    
 public:
  int setup();
  double run();
};

#endif
