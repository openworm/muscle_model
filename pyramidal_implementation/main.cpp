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
using namespace std;

class PyramidalSimulation{

private:
  PyObject *pName, *pModule, *pDict, *pFunc, *pValue, *pClass, *pInstance;    

public:

  int setup(){

    char python_module[] = "main_test";
    char method[] = "test_function";
    char pyClass[] = "test_simulation";

    Py_Initialize();
    pName = PyString_FromString("main_test");
    pModule = PyImport_Import(pName);

    //    // Build the name of a callable class         
    if (pModule != NULL){
      pClass = PyObject_GetAttrString(pModule,"test_simulation");
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
  }


  double run(){
    // Call a method of the class with no parameters, example here is to call it twice:                   
    double membranePotential;
    pValue = PyObject_CallMethod(pInstance, "run", NULL);
    
    return PyFloat_AsDouble(pValue);
  }
  
  
};


int main(){

  PyramidalSimulation simulation;
  simulation.setup();
  double potential;

  int i;
  i = 0;

  //example usage, run a hundred increments with the default value (set in python)

  while (i < 100) {
    potential = simulation.run();
    cout << potential<<endl;
    i++;
  }
  return 0;
}
