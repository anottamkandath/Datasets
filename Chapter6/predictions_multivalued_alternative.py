from cornetto.simcornet import SimCornet
from collections import defaultdict
from operator import itemgetter
import rdflib
import sys

c = SimCornet()
c.open("/Users/dceolin/pycornetto-0.6/bin/cdb_lu_subcounts.xml", "/Users/dceolin/pycornetto-0.6/bin/cdb_syn_counts.xml")
train = rdflib.Graph()
train.parse("data_2.rdf")
test = rdflib.Graph()
test.parse("data_3.rdf")

values = [1.0,2.0,3.0,4.0,5.0]

def opinion_tag(t1,tags):
 try:
  p = [(t[1],c.lin_sim(t2.toPython(),v.toPython())) 
 		for t2 in test.objects(t1[0],rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody")) 
 		for t in tags 
 		for v in train.objects(t[0],rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody"))]
  d1 = dict([(x,[0.0]) for x in values])
  for v,w in p:
   if (w==None):
    d1[v].append(0.0)
   else:
    d1[v].append(w)
  d = dict(d1)
  res = dict((a,float(sum(b)+1.0)/float(sum([item for sublist in d.values() for item in sublist])+len(d))) for a,b in d.iteritems())
  #try:
  # res['uncertainty'] = float(len(d))/float(sum([item for sublist in d.values() for item in sublist])+len(d))
  #except:	
  # res['uncertainty'] = 1.0
 except:
  #res = dict([('uncertainty',1.0)])
  res = dict([(x,0.2) for x in values])
 return (t1[0],res)

def opinion_all_tags(testset,trainingset):
	a = [opinion_tag(x,trainingset) for x in testset]
	return a	

def create_reputation():
	users = list(set([o for s,o in train.subject_objects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"))]))
	res=[]
	for u in users:
		rep = dict([(x,0.0) for x in values])
		for a in train.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"),u):
			for a1,p1,o in train.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),a)):
				for v in train.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody")):
					if(v.toPython()!="typo" and v.toPython()!="?"):
						rep[float(v.toPython())] = rep[float(v.toPython())]+ 1.0
		e = dict([(float(x),float(y+1)/((sum(rep.values())+len(rep)))) for (x,y) in rep.iteritems()])
		res.append((u,e))
	return res

def predict():
	users = list(set([o for s,o in test.subject_objects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"))]))
	print "users:",len(users)
	annotations_eval = dict([(user,
							[(a,float(v.toPython())) 
								for a in train.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"),user) 
								for a1,p1,o in train.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),a)) 
								for v in train.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody"))
								if (v.toPython()!="typo" and v.toPython()!="?")
							]) 
						for user in users])
	annotations_to_be_eval = dict([(user,
							[(a,float(v.toPython())) 
								for a in test.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"),user) 
								for a1,p1,o in test.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),a)) 
								for v in test.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody"))
								if (v.toPython()!="typo" and v.toPython()!="?")
							]) 
						for user in users])
	#print "annotations_to_be_eval:",len(annotations_to_be_eval)
	evaluations = dict([(user,opinion_all_tags(annotations_to_be_eval[user],annotations_eval[user])) for user in users])
	#print "evaluations: ",sum([len(x) for x in evaluations.values()])
	res = []
	for user in users:
		try:
			r = reputations[user]
		except:
			r = [(x,1.0/len(values)) for x in values]
		e = evaluations[user]
		l = len(e)
		accept = [(x,round(l*y)) for (x,y) in r.iteritems()]	# number of accepted items per evaluation score
		accept[0] = (values[0],l-sum(dict(accept[1:]).values()))
		accept = dict(accept)
		#print accept
		while(sum(accept.values())>0):
			e = sorted(e,key=lambda o:max(o[1].values()))
			#print e
			k = e[0][1].keys()[e[0][1].values().index(max(e[0][1].values()))] #.key(max(e[0][1].values()))
			#print k
			if(accept[k]>0):
				accept[k] = accept[k]-1
				#if(accept[k]==0):
				#	del accept[k]
				res.append((e[0][0],k))
				e.pop(0)
			else:
				del e[0][1][k]	
	#for user in users:
	#	try:
	#		r = reputations[user]
	#	except:
	#		r = [(x,1.0/len(values)) for x in values]
	#	e = evaluations[user]
	#	l = len(e)
	#	accept = [(x,round(l*y)) for (x,y) in r.iteritems()]	# number of accepted items per evaluation score
	#	accept[0] = (values[0],l-sum(dict(accept[1:]).values()))
	#	accept = sorted(accept, reverse=True)
	#	for (x,y) in accept:
	#		try:
	#			e = sorted(e, key=lambda o: o[1][int(x)])
	#		except:
	#			print o[1]
	#		for i in range (0,int(y)):
	#			res.append((e[0][0],x))
	#			e.pop(0)
	return res	

def validated_tags():
	annotations = [(s,(float(v.toPython()))) 
					for s in test.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator")) 
					for a1,p1,o in test.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),s)) 
					for v in test.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody")) 
					if (v.toPython()!="typo" and v.toPython()!="?")]
					
	return annotations

def evaluate_program():
		validated = validated_tags()
		p = predict()
		predicted = dict(p)
		print len(p),len(validated)
		true = 0
		false = 0
		for x in validated:
			if (x[1] == predicted[x[0]]):
				true = true + 1
			else:
				false = false + 1
		accuracy = float(true)/(true+false)
		print "true:",true
		print "false:",false
		print "accuracy: ", accuracy
	#except:
	#	print sys.exc_info()
	#return true_positive,true_negative,false_positive,false_negative

#create_reputation()
reputations = dict(create_reputation())	
#result = predict()
#print result
evaluate_program()
#print(reputations)