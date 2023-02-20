# Assessment_of_risk_subpopulation_of_stem_cells
This repository shows a cell quality assessment pipeline established using bioinformatics and machine learning methods. Single cell gene expression data (obtained from the scRNA-seq experiment) and cell phenotype were used as input data.

# Software installation.
Please refer to our published protocol artice “Assessment of risk sub-population of stem cells” for step-by-step installation code.

# Data preprocessing.
  1. Raw data quality control and filtering.
  2. Building the cell-gene expression seurat object.
  3. Normalization, remove of the batch effect and clustering analysis.
  
  The detailed code of this part has been shown in our published protocol artice “Assessment of risk sub-population of stem cells”.

# Feature selection.
  4. Set up training and test sets. 
    You can use the script "script/RandomSelectCellsAndHVG2000Exp.pl" in this repository to complete this step according to our published article.
  5. Label the class of cells.
    You can use the script "script/add_typeToinput.pl" in this repository to complete this step according to our published article.
  6. Rank the importance of features and determine the optimal feature number.
  7. Count the cross validation accuracy of different C-value models under different feature numbers to determine the optimal number of important features

# Training classifier 8. Develop machine learning strategies. 
  9. Import cell instances of the training set. 
  10. Establish SVM machine learning framework. 
  11. Obtain the 13 most important feature genes and their expression levels. 
  12. Train classifiers and output their performance. 
  13. Change the super parameter C value and repeat steps 10, 11 and12.

# Test and determine the optimal classifier 
  14. Import test set 1 cell instances. 
  15. Test the performance of the candidate classifier 1 in test set 1. 
  16. Output classifier 1 parameters. 
  17. Repeat steps 15 and 16to test the performance of all 14 candidate classifiers in test set 1. 
  18. Repeat steps 14, 15, 16 and 17to test the performance of all 14 candidate classifiers in test set 2, 3 and 4. 
  19. Determine the optimal classifier.

# Development of mathematical model for embolic risk of ADSC cell
  20. After getting the gene expression profile of a cell, extract the expression amount of its 13 key genes, and then calculate the embolic risk of the cell.
  21. Select an appropriate risk threshold according to the cell production process and determine whether the cell is a pro-embolic cell
  22. Calculate the proportion of embolic cells in the sample, and predict the embolic possibility of reinfused individuals according to the established regression relationship between the embolic cell proportion and the embolic risk after reinfusion.

All detailed code of this pipeline has been shown in our published protocol artice “Assessment of risk sub-population of stem cells”, please refer to it to create a pipeline.
