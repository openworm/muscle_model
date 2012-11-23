// to compile and run (temp notes with hardcoded paths) 
// run the following commands from inside curdir:
// 
// $ export PYTHONPATH="/home/mike/dev/cpp_pyramidal_integration/"
//OR
//export PYTHONPATH=$PYTHONPATH:/home/mike/dev/muscle_model/pyramidal_implementation/
// $ g++ main.cpp -l python2.7 -o sim -I /usr/include/python2.7/
// $ ./sim

#include <Python.h>
#include <iostream>
#include "PyramidalSimulation.h"

using namespace std;

int PyramidalSimulation::setup(){

  char python_module[] = "main";
  char pyClass[] = "muscle_simulation";

  Py_Initialize();
  pName = PyString_FromString(python_module);
  pModule = PyImport_Import(pName);

  //    // Build the name of a callable class         
  if (pModule != NULL){
    pClass = PyObject_GetAttrString(pModule,pyClass);
  }
  else {
    cout << "Module not loaded, have you set PYTHONPATH?" <<endl;
  }
    
  // Create an instance of the class                                                                    
  if (PyCallable_Check(pClass))
    {
      pInstance = PyObject_CallObject(pClass, NULL);
    }
  else {
    cout << "Pyramidal simulation class not callable!"<<endl;
  }

  return 0;
};


double PyramidalSimulation::run(){
  // Call a method of the class
  double membranePotential;
  pValue = PyObject_CallMethod(pInstance, "run", NULL);
  
  return PyFloat_AsDouble(pValue);
};

