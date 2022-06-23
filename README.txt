To work with this project you have to do the next things:
    1.  Change the variables from lines 88 up to and including 95 to what you want it to be
        that will be used in the LFR benchmark function to generate new graphs.
    2.  Run the code.
    3.  The results will be visible in EdgeRatio.csv and Modularity.csv

The code will run louvain_getCommunities from Louvain.py which uses the class functions from
MeasureInterface. These functions are explicit defined in the files of the Measure folder.
To add new heuristics with new measures you have to add a new file into this folder and you 
have to change the value of variable measureToRun in the Main.py. The value of this variable
should be of the same name of the file name.