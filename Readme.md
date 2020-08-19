Main Executable: tsp_R00184198.py
Description: Main Executable or index file of the program. 
Please execute using:
		python tsp_R00184198.py inst-16.tsp

inst-16.tsp is the file name. File should be present in TSPdataset folder.

Program will ask for user input:
	Please choose configuration from below:
		1 : ['random', 'uniformCrossover', 'inversionMutation', 'randomSelection']
		2 : ['random', 'pmxCrossover', 'reciprocalExchangeMutation', 'randomSelection']
		3 : ['random', 'uniformCrossover', 'reciprocalExchangeMutation', 'stochasticUniversalSampling']
		4 : ['random', 'pmxCrossover', 'reciprocalExchangeMutation', 'stochasticUniversalSampling']
		5 : ['random', 'pmxCrossover', 'inversionMutation', 'stochasticUniversalSampling']
		6 : ['random', 'uniformCrossover', 'inversionMutation', 'stochasticUniversalSampling']
		7 : ['NearestNeighbour', 'pmxCrossover', 'inversionMutation', 'stochasticUniversalSampling']
		8 : ['NearestNeighbour', 'uniformCrossover', 'inversionMutation', 'stochasticUniversalSampling']

please select a configuration from below using the number next to the configuration (1-8).

Program will execute and display in command prompt/editor the current iteration number, best fitness till the iteration.
Program on completion will save plot of min/max/mean/best/median fitness per iteration in files folder as configuration {user input}.png.
Program will also save config, execution time, best fitness and distance in configstats.csv file of files folder for each execution.
Error logs on any error will be save to lot.txt of files folder.
Files folder contains data and plots of the previous runs for review if required, same are used in the report. 

If user wants to change population or mutation rate, same can be adjusted by changing below line of code:
	ga = BasicTSP(problem_file, 300, 0.5, 500)

Individual.py is moved to folder prolibs as part of modularization. plotmodule.py is used to plot data. 

Required Libraries(other thank core python): numpy, matplotlib, statistics



Description on Changes done to the original Code
-------------------------------------------------------
1) Fitness function individual.computeFitness() has been modified to get fitness as Inverse of euclidean distance. 
   This transformaton is for acheiving Minimisation objective.
2) UpdateMating Pool function name changed to randomSelection
3) randomselection function renamed to randomparentSelection"# geneticalgorithms-tsp" 
