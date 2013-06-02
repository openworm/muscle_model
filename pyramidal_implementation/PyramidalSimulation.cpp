// The MIT License (MIT)
//
// Copyright (c) 2011, 2013 OpenWorm.
// http://openworm.org
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the MIT License
// which accompanies this distribution, and is available at
// http://opensource.org/licenses/MIT
//
// Contributors:
//      OpenWorm - http://openworm.org/people.html
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
// USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import with_statement
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

