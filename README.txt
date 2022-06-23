To work with this project you have to do the next things:
    1.  Change the variables from lines 88 up to and including 95 to what you want it to be
        that will be used in the LFR benchmark function to generate new graphs.
    2.  Change the used measure, this is done by changing measureToRun on line 11 of Main.py.
    3.  Run Main.py.
    4.  The results will be visible in a csv file in the root of this repository.

Create new measure:
    1.  Add a new python script with desired measure name in the Measures folder.
    2.  Import MeasureInterface import MeasureInterface.
    3.  Create a new Measure which inherits MeasureInterface.
    4.  Implement getTotalMeasure and getDelta. Note, the Louvain algorithm maximises the measure.
    5.  Add your file as an import from the Measures folder in Main.py.
    6.  Change the measure on line 11 of Main.py.
    7.  Run your Measure.

