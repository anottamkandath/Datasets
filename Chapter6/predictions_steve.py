from cornetto.simcornet import SimCornet
from collections import defaultdict
from operator import itemgetter
import rdflib
from nltk.corpus import wordnet

#c = SimCornet()
#c.open("/Users/dceolin/pycornetto-0.6/bin/cdb_lu_subcounts.xml", "/Users/dceolin/pycornetto-0.6/bin/cdb_syn_counts.xml")

train = rdflib.Graph()
train.parse("train.rdf")
test = rdflib.Graph()
test.parse("test.rdf")

def opinion_tag(t1,tags):
 try:
  p = [((t[1]=="usefulness-useful"),max([x.wup_similarity(nltk.corpus.wordnet.synset(v.toPython())) for x in nltk.corpus.wordnet.synsets(t2.toPython())])) 
 		for t2 in test.objects(t1[0],rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody")) 
 		for t in tags 
 		for v in train.objects(t[0],rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody"))]
  d1 = defaultdict(list)
  for v,w in p:
   if (w==None):
    d1[v].append(0)
   else:
    d1[v].append(w)
  d = dict(d1)
 #dict((a,float(sum(b))/float(sum(d)+len(d))) for a,b in d.iteritems())
 #try:
 # d['uncertainty'] = float(len(d))/float(sum(d)+len(d))
 #except:	
 # d['uncertainty'] = 1
  e = d[1]/(d[1]+d[0]+2)
 except:
  e = 0.5
 return (t1[0],e)

def opinion_all_tags(testset,trainingset):
	a = [opinion_tag(x,trainingset) for x in testset]
	b = sorted(a, key=lambda opinion: opinion[1])
	return b	

def create_reputation():
	users = list(set([o for s,o in train.subject_objects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"))]))
	res=[]
	for u in users:
		p = 0
		n = 0
		for a in train.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"),u):
			for a1,p1,o in train.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),a)):
				for v in train.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody")):
					if(v.toPython()!="typo" and v.toPython()!="?"):
						if (v.toPython()=="usefulness-useful"):
							p = p + 1
						else:
							n = n + 1
		e = (float(p)+1)/float(p+n+2)				
		res.append((u,e))
	return res

def predict():
	users = list(set([o for s,o in test.subject_objects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"))]))
	annotations_eval = dict([(user,
							[(a,v.toPython()) 
								for a in train.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"),user) 
								for a1,p1,o in train.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),a)) 
								for v in train.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody"))
								if (v.toPython()!="typo" and v.toPython()!="?")
							]) 
						for user in users])
	annotations_to_be_eval = dict([(user,
							[(a,v.toPython()) 
								for a in test.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"),user) 
								for a1,p1,o in test.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),a)) 
								for v in test.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody"))
								if (v.toPython()!="typo" and v.toPython()!="?")
							]) 
						for user in users])
	evaluations = dict([(user,opinion_all_tags(annotations_to_be_eval[user],annotations_eval[user])) for user in users])
	res = []	
	for user in users:
		try:
			r = reputations[user]
		except:
			r = 0.5
		e = evaluations[user]
		l = len(e)
		accept = round(l*r)
		i = 1
		for e1 in e:
			if(i<=accept):	
				res.append((e1[0],True))
			else:
				res.append((e1[0],False))
			i = i + 1
	print res[0]
	return res

def validated_tags():
	annotations = [(s,(v.toPython())=="usefulness-useful") 
		for s in test.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator")) 
		for a1,p1,o in test.triples((None,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),s)) 
		for v in test.objects(a1,rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasBody")) 
		if (v.toPython()!="typo" and v.toPython()!="?")]
	return annotations

def evaluate_program():
	validated = validated_tags()
	p = predict()
	predicted = dict(p)
	true_positive = 0
	true_negative = 0
	false_positive = 0
	false_negative = 0
	for x in validated:
		if (x[1] == predicted[x[0]]):
			if (x[1]==0):
				true_negative = true_negative + 1
			else:
				true_positive = true_positive + 1
		else:
			if (x[1]==0):
				false_positive = false_positive + 1
			else:
				false_negative = false_negative + 1
	print("true negative",true_negative)
	print("true positive",true_positive)
	print("false positive",false_positive)
	print("false negative",false_negative)
	accuracy = float((true_positive+true_negative)) / float(len(validated))
	precision = true_positive/float(true_positive+false_positive)
	recall = true_positive / float(true_positive + false_negative)
	print "accuracy: ", accuracy
	print "precision: ", precision
	print "recall: ", recall
	print "f-measure: ",2*(precision*recall)/(precision+recall)
	#return true_positive,true_negative,false_positive,false_negative

#create_reputation()
reputations = dict(create_reputation())	
#result = predict()
#print result
evaluate_program()
#print(reputations)