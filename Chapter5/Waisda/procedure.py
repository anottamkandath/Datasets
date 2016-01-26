import os
import sys
import csv
import time
import numpy
import math
import cmath

def comp(threshold = 0.75, min_evidence = 4):
	test = csv.reader(open('data_testset.csv', 'rb'), delimiter=',')
	#ofile = open('data_result.csv', 'wb')
	#out = csv.writer(ofile, delimiter=' ')
	true_positive = 0
	true_negative = 0
	false_positive = 0
	false_negative = 0
	true_positive_prov = 0
	true_negative_prov = 0
	false_positive_prov = 0
	false_negative_prov = 0
	true_positive_avg = 0
	true_negative_avg = 0
	false_positive_avg = 0
	false_negative_avg = 0

	for row in test:
		train = csv.reader(open('data_trainset.csv', 'rb'), delimiter=',')
		p = 0
		n = 0
		if(row[13]=='creationDate'):
			continue
		count = 0
		for row2 in train:
			if(row2[10] == row[10] and time.strptime(row[13],'%Y-%m-%d %H:%M:%S')>time.strptime(row2[13],'%Y-%m-%d %H:%M:%S')):
				p = p + (float(row2[19]))/(float(row2[19])+1)
				n = n + (1/(float(row2[19])+1))
				count = count + 1
				#print("p "+str(p))
		e = (p + 1) / (p +n+2)
		prov = csv.reader(open('prediction_matches.csv', 'rb'), delimiter=',')
		for row_prov in prov:
			if(row_prov[0] == row[0]):
				p = float((6+int(row_prov[1])))/float(10)
				#print("---"+str(p))
				break
		if(count>=min_evidence):
			e2 = e
		else:
			e2 = p
		e3 = (float(e) + float(p))/2
		#print("---")
		#print(p)
		#print(e)
		#print(e2)
		#print(e3)
		r = (float(row[19]))/(float(row[19])+1)
		#print(e)
		#print(r)
		if(r>threshold):
			if(e>threshold):
				true_positive = true_positive + 1
			else:
				false_negative = false_negative + 1
			if(e2>threshold):
				true_positive_prov = true_positive_prov + 1
			else:
				false_negative_prov = false_negative_prov + 1
			if(e3>0.75):
				true_positive_avg = true_positive_avg + 1
			else:
				false_negative_avg = false_negative_avg + 1
		else:
			if(e>threshold):
				false_positive = false_positive + 1
			else:
				true_negative = true_negative + 1
			if(e2>threshold):
				false_positive_prov = false_positive_prov + 1
			else:
				true_negative_prov = true_negative_prov + 1
			if(e3>threshold):
				false_positive_avg = false_positive_avg + 1
			else:
				true_negative_avg = true_negative_avg + 1
			
	print("true positive: "+str(true_positive))
	print("true negative: "+str(true_negative))
	print("false positive: "+str(false_positive))
	print("false negative: "+str(false_negative))
	print("accuracy: "+str(float(true_positive+true_negative)/float(true_positive+true_negative+false_positive+false_negative)))
	print("true positive prov: "+str(true_positive_prov))
	print("true negative prov: "+str(true_negative_prov))
	print("false positive prov: "+str(false_positive_prov))
	print("false negative prov: "+str(false_negative_prov))
	print("accuracy prov: "+str(float(true_positive_prov+true_negative_prov)/float(true_positive_prov+true_negative_prov+false_positive_prov+false_negative_prov)))
	print("true positive avg: "+str(true_positive_avg))
	print("true negative avg: "+str(true_negative_avg))
	print("false positive avg: "+str(false_positive_avg))
	print("false negative avg: "+str(false_negative_avg))
	print("accuracy avg: "+str(float(true_positive_avg+true_negative_avg)/float(true_positive_avg+true_negative_avg+false_positive_avg+false_negative_avg)))



def comp2():
	f = open('results_zeros_abs_fine_1000.csv', 'wt')
	f2 = open('reputations_fine.csv','wt')
	writer = csv.writer(f)
	writer2 = csv.writer(f2)
	writer.writerow(('min_evidence','threshold','accuracy norm','accuracy prov','accuracy avg','true positive norm','true negative norm','false positive norm','false negative norm','true positive prov','true negative prov','false positive prov','false negative prov','true positive avg','true negative avg','false positive avg','false negative avg'))
	for min_evidence in range(2,3):
		test = csv.reader(open('data_testset.csv', 'rb'), delimiter=',')
		true_positive= numpy.zeros(10)
		true_negative= numpy.zeros(10)
		false_positive = numpy.zeros(10)
		false_negative = numpy.zeros(10)
		true_positive_prov = numpy.zeros(10)
		true_negative_prov = numpy.zeros(10)
		false_positive_prov = numpy.zeros(10)
		false_negative_prov = numpy.zeros(10)
		true_positive_avg = numpy.zeros(10)
		true_negative_avg = numpy.zeros(10)
		false_positive_avg = numpy.zeros(10)
		false_negative_avg = numpy.zeros(10)
		accuracy_norm = numpy.zeros(10)
		accuracy_prov = numpy.zeros(10)
		accuracy_avg = numpy.zeros(10)
		prov = csv.reader(open('prediction_matches_zeros_abs_fine.csv', 'rb'), delimiter=',')
		row_prov = prov.next()	
		for row in test:
			train = csv.reader(open('data_trainset.csv', 'rb'), delimiter=',')
			p = 0
			n = 0
			count = 0
			pr = 0
			if(row[13]=='creationDate'):
				continue
			for row2 in train:
				if(row2[10] == row[10] and time.strptime(row[13],'%Y-%m-%d %H:%M:%S')>time.strptime(row2[13],'%Y-%m-%d %H:%M:%S')):
					p = p + (float(row2[19])-1)/(float(row2[19]))
					n = n + (1/(float(row2[19])))
					count = count + 1
			e = (p + 1) / (p +n+2)
			#prov = csv.reader(open('prediction_matches_zeros.csv', 'rb'), delimiter=',')
			#for row_prov in prov:
			#	if(row_prov[0] == row[0]):
			#		pr = (5+(float(row_prov[1])-1)/2)/10
			#		break
			row_prov = prov.next()
			pr = (5+(float(row_prov[1])-1)/2)/10+0.025
			#print(min_evidence,count)
			if(count>=min_evidence):
				e2 = e
			else:
				e2 = pr
			e3 = pr
			r = (float(row[19])-1)/(float(row[19]))
			r = (round(r*10000))
			e_save=e
			e = round(e*10000)
			e2 = round(e2*10000)
			e3 = round(e3*10000)
			for threshold in [(float(i)/2+5)/10 for i in range(0,10)]:
				j = int((threshold*10 - 5)*2)
				threshold = math.floor(threshold*10000)				
				if(r>threshold):
					if(e>threshold):
						true_positive[j] = true_positive[j] + 1
					else:
						false_negative[j] = false_negative[j] + 1
					if(e2>threshold):
						true_positive_prov[j] = true_positive_prov[j] + 1
					else:
						false_negative_prov[j] = false_negative_prov[j] + 1
					if(e3>threshold):
						true_positive_avg[j] = true_positive_avg[j] + 1
					else:
						if(threshold==9500):
							print("false negative")
							print(e3,r,threshold)
						false_negative_avg[j] = false_negative_avg[j] + 1
				else:
					if(e>threshold):
						false_positive[j] = false_positive[j] + 1
					else:
						true_negative[j] = true_negative[j] + 1
					if(e2>threshold):
						false_positive_prov[j] = false_positive_prov[j] + 1
					else:
						true_negative_prov[j] = true_negative_prov[j] + 1
					if(e3>threshold):
						if(threshold==9500):
							print(e3,r,threshold)	
							print("false positive")
						false_positive_avg[j] = false_positive_avg[j] + 1
					else:
						true_negative_avg[j] = true_negative_avg[j] + 1
			writer2.writerow((pr-0.025,e_save,count))			
		for j in range(0,10):
			accuracy_norm[j] = float(true_positive[j]+true_negative[j])/float(true_positive[j]+true_negative[j]+false_positive[j]+false_negative[j])
			accuracy_prov[j] = float(true_positive_prov[j]+true_negative_prov[j])/float(true_positive_prov[j]+true_negative_prov[j]+false_positive_prov[j]+false_negative_prov[j])
			accuracy_avg[j] = float(true_positive_avg[j]+true_negative_avg[j])/float(true_positive_avg[j]+true_negative_avg[j]+false_positive_avg[j]+false_negative_avg[j])
			writer.writerow((min_evidence,float(j)/2+5,accuracy_norm[j],accuracy_prov[j],accuracy_avg[j],true_positive[j],true_negative[j],false_positive[j],false_negative[j],true_positive_prov[j],true_negative_prov[j],false_positive_prov[j],false_negative_prov[j],true_positive_avg[j],true_negative_avg[j],false_positive_avg[j],false_negative_avg[j]))
	f.close()
	f2.close()
	
comp2()