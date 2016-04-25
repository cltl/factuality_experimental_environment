Evaluation of entities and relations annotation in CAT XML labelled format
-------------------------------------------------------------------------------

USAGE
To evaluate files annotated by a system against gold standard:
> python scorer_CAT.py folder_gold/ folder_system/ list_class_att [debug] [output_file]

debug = 0, no print on the standard output
debug = 3, prints TLINK annotation to check problem
debug = 4, prints triples build from TLINK

output_file = an empty file in txt or csv

OUTPUT
The output file will contain the evaluation in CSV format. If no argument is given, then the results will be written to stdout.


EVALUATION METHODOLOGY
* For each markable two evaluations are done: strict matching and relaxed matching. For example, if the gold annotation contains "Tuesday evening" and the system detects "Tuesday", then they will get credit in relaxed matching but not in exact matching.
We compute the accuracy of attribute value by taking into consideration only matched markables.

Example:
Markables	TP	FP	FN	recall	precision	f-measure	accuracy att
TIMEX3							type	value	
	8	1.0	3.0	0.727272727273	0.888888888889	0.8	1.0	1.0	
TIMEX3(relaxed match)							type	value	
	9	0.0	2.0	0.818181818182	1.0	0.9	1.0	1.0	
	

* For each relation we provide two evaluations: strict matching and relaxed matching. In the first case two relations match if their sources and their targets strictly match, as well as their non-optional attributes. In the second case, a relaxed matching is considering between the sources and the targets. 

The TLINK relations are also evaluated using the evaluation methodology of (UzZaman and Allen, 2011). This evaluation has been used for the TempEval3 task (UzZaman et al., 2013). In the output results we call this evaluation "tempeval evaluation".

Example:
Relations	TP	FP	FN	recall	precision	f-measure	accuracy att	
TLINK (tempeval evaluation)							relType	
	24	2.0	4.0	0.857142857143	0.923076923077	0.888888888889	1.0	
TLINK							relType	
	24	2.0	4.0	0.857142857143	0.923076923077	0.888888888889	1.0	
TLINK (relaxed match)							relType	
	25	1.0	3.0	0.892857142857	0.961538461538	0.925925925926	1.0


CONFIG
The list_class_att file contains one line by annotation type with the following format:
NAME	type(markable|one2one|many2one|instance)	specificity(directional|undirectional|comparable|non-comparable|0)	list_attribute

Specificity: directional and undirectional should be used for relation; comparable and non-comparable indicate if the evaluation on "instance" could be computed; 0 is used for markable. 

The list_attribute is a list of attribute split up by tabulation. The lines begining by # are ignored.

Example:
# markable
EVENT	markable	0	class
TIMEX3	markable	0	type	value
# one2one
TLINK	one2one	directional	relType
# instance
TIMEX3	instance	non-comparable	type	value


EXTERNAL TOOL
This evaluation module relies partly on the TempEval 2013 evaluation toolkit (http://www.cs.york.ac.uk/semeval-2013/task1/index.php?id=data) for the evaluation of TLINK. It uses the script relation_to_timegraph.py. To run the EVALITA scorer, download the Evaluation Tool Kit from the TempEval-3 website (http://www.cs.rochester.edu/~naushad/tempeval3/tools.zip) and put the relation_to_timegraph.py script (the script is located in the folder "evaluation-relations") in the same folder of the EVALITA scorer, then launch the command.

REFERENCES
N. UzZaman and J. Allen. 2011. Temporal Evaluation. In Proceedings of The 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies.
Naushad UzZaman, Hector Llorens, James F. Allen, Leon Derczynski, Marc Verhagen, and James Pustejovsky. Tempeval-3: Evaluating events, time expressions, and temporal relations. CoRR, abs/1206.5333, 2012.


AUTHOR
Anne-Lyse Minard (minard@fbk.eu)


LAST UPDATED
June 18, 2014. 
