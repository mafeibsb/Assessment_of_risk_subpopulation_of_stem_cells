import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score,cross_validate
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report,log_loss
from sklearn import svm
from sklearn.feature_selection import RFE,RFECV
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


input=sys.argv[1]
rfecv_dir=sys.argv[2]
c_use=float(sys.argv[3])
method=sys.argv[4]
function=sys.argv[5]
print(input)
#input="/work1/xuelab/project/mafei/project/10.AA_FA/output/23.sklearn_analysis/4.copy_analysis/GeneInt_selected.txt"
raw_data=pd.read_csv(input,index_col=0,header='infer',sep='\t',low_memory=False)

raw_data=raw_data[raw_data.columns[np.sum(raw_data)!=0]]

x=raw_data.drop('type',axis=1)
y=raw_data['type']

raw_embolic=raw_data[raw_data['type']=='embolic']
x_embolic=raw_embolic.drop('type',axis=1)
y_embolic=pd.DataFrame(raw_embolic['type'])
raw_nonembolic=raw_data[raw_data['type']=='nonembolic']
x_nonembolic=raw_nonembolic.drop('type',axis=1)
y_nonembolic=pd.DataFrame(raw_nonembolic['type'])

x_embolic_train, x_embolic_test, y_embolic_train, y_embolic_test = train_test_split(x_embolic, y_embolic, random_state=1, train_size=0.7, test_size=0.3)
x_nonembolic_train, x_nonembolic_test, y_non-embolic_train, y_nonembolic_test = train_test_split(x_nonembolic, y_nonembolic, random_state=1, train_size=0.7, test_size=0.3)


x_test=pd.concat([x_embolic_test,x_nonembolic_test],axis=0)
y_test=pd.concat([y_embolic_test,y_nonembolic_test],axis=0)['type']
x_train=pd.concat([x_embolic_train,x_nonembolic_train],axis=0)
y_train=pd.concat([y_embolic_train,y_nonembolic_train],axis=0)['type']

cv=10
#c_all=[0.2,0.6,1,1.2,1.6,2]
#methods=['linear', 'poly', 'rbf', 'sigmoid']
#functions=['ovo','ovr']
#for method in methods:
#	for function in functions:
#		for c_use in c_all:
clf = svm.SVC(C=c_use, kernel=method, gamma='auto', decision_function_shape=function, probability = True,class_weight='balanced',cache_size=2000)
			
rfecv=RFECV(estimator=clf, step=1, cv=cv, scoring='accuracy')
rfecv.fit(x, y)
rfecv_numb=rfecv.n_features_
			
pdf=PdfPages(rfecv_dir+'/svm_'+input.split('/')[-1].strip('.txt')+'_'+function+'_'+str(c_use)+'_'+method+'.pdf')
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation Accuracy")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()
pdf.savefig()
plt.close()
pdf.close()
ref_txt=rfecv_dir+'/svm_'+input.split('/')[-1].strip('.txt')+'_'+function+'_'+str(c_use)+'_'+method+'.txt'
pd.DataFrame(rfecv.grid_scores_, columns=['socre']).to_csv(ref_txt,index=False,header=False)
			
rfe = RFE(estimator=clf, n_features_to_select=1)
rfe.fit(x, y)
ranking=sorted(zip(rfe.ranking_,x.columns))
print(function,rfecv_numb,ranking)
'''
			x_train_new=x_train[gene_list]
			x_test_new=x_test[gene_list]
			clf = svm.SVC(C=c_use, kernel=method, gamma='auto', decision_function_shape=function, probability = True,class_weight='balanced')
			clf.fit(x_train_new, y_train.ravel())
			
			munb=y_train.shape[0]
			for i in set(y_train):
				munb=min(munb, y_train[y_train==i].shape[0])

			for i in range(10):
				scores=cross_val_score(clf, x_train_new, y_train, cv=cv, error_score='raise-deprecating', scoring='accuracy')
				print("cross validation Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 1.96))
				print(scores)
			
			#clf.score(x_train_new, y_train)
			
			sys.path.append('/work1/xuelab/project/wenh/project/10.AA_FA/bin/23.sklearn_analysis')
			import print_matrix
			y_pred=clf.predict(x_train_new)
			y_proba = clf.predict_proba(x_train_new)
			numb1=print_matrix.count_numb(list(y_train),list(y_pred))
			print(numb1)
			
			y_pred = clf.predict(x_test_new)
			y_proba = clf.predict_proba(x_test_new)
			numb2=print_matrix.count_numb(list(y_test),list(y_pred))
			print(numb2)
			
			accuracy=accuracy_score(y_test,y_pred)
			print("Classification Accuracy: %0.2f" %accuracy)
			
			#confusion=confusion_matrix(y_test,y_pred)
			
			#classifi=classification_report(y_test, y_pred)
			
			#logloss=log_loss(y_test, y_proba)
			
			clf2 = svm.SVR(C=0.8, kernel=method, gamma='auto')
			'''

