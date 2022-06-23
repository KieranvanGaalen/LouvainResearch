To work with this project you have to do the next things:
    1.  Change the variables from lines 88 up to and including 95 to what you want it to be
        that will be used in the LFR benchmark function to generate new graphs.
    2.  Change the used measure, this is done by changing measureToRun on line 11 of Main.py
    3.  Run Main.py.
    4.  The results will be visible in a csv file in the root of this repository.

The code will run louvain_getCommunities from Louvain.py which uses the class functions from
MeasureInterface. These functions are explicit defined in the files of the Measure folder.
To add new heuristics with new measures you have to add a new file into this folder which implements
the MeasureInterface, and you have to change the value of variable measureToRun in the Main.py. 
The value of this variable should be of the same name of the file name.