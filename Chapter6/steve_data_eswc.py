import MySQLdb
import rdflib
from rdflib.graph import Graph
from rdflib import Literal, BNode, Namespace, URIRef
from rdflib import RDF
import math
import sys
reload(sys)

def oa():
	try:
		db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="steve")
		db.set_character_set('utf8')
		db.query("select steve_term.term_id as AnnotationId, steve_term.term_norm as Tag, steve_term.entered_dtm as AnnotationTime, steve_term.mime_id as ImageID, steve_session.user_id,steve_term_review.term_review_id as ReviewId, steve_term_review.entry_time as ReviewTime, steve_term_review.user_id as ReviewerID, steve_term_review.term_str as AnnReviewd, steve_term_review.evaluation as Review from steve_term, steve_session, steve_term_review where steve_term.session_id = steve_session.session_id and `steve_term_review`.mime_id = steve_term.mime_id and steve_term.term_norm = steve_term_review.term_str order by user_id, ReviewTime")
		r = db.store_result()
		rows = r.fetch_row(how=1,maxrows=0)
		g = Graph()
		train = rdflib.Graph()
		test = rdflib.Graph()
		g.bind("oa","http://www.w3.org/ns/openannotation/core/")
		OA = Namespace("http://www.w3.org/ns/openannotation/core/")
		i = 0
		user_tmp = rows[0]['user_id']
		for item in rows:
			tagEntry = URIRef("http://steve.nl/"+str(item['AnnotationId']))
			user = URIRef("http://steve.nl/user_"+str(item['user_id']))
			tag = URIRef("http://steve.nl/tag_"+str(item['ImageID']))
			review = URIRef("http://steve.nl/review_"+str(item['ReviewId']))
			reviewer = URIRef("http://steve.nl/reviewer_"+str(item['ReviewerID']))
			if(user_tmp==item['user_id']):
				i = i + 1
			else:
				i = 0
				user_tmp = item['user_id']
			if(i<=5):
				train.add((tagEntry, RDF.type, OA["annotation"]))
				train.add((tagEntry, OA["hasBody"], Literal(str(item['Tag']))))
				train.add((tagEntry, OA["annotator"], user))
				train.add((tagEntry, OA["hasTarget"], tag))
				train.add((tagEntry, OA["annotated"], Literal(item['AnnotationTime'])))
				train.add((review, RDF.type, OA["annotation"]))
				train.add((review,OA["hasBody"],Literal(str(item['Review']))))
				train.add((review,OA["hasTarget"],tagEntry))
				#train.add((review,OA["annotator"],reviewer))
				train.add((review,OA["annotated"],Literal(item['ReviewTime'])))
			else:
				test.add((tagEntry, RDF.type, OA["annotation"]))
				test.add((tagEntry, OA["hasBody"], Literal(str(item['Tag']))))
				test.add((tagEntry, OA["annotator"], user))
				test.add((tagEntry, OA["hasTarget"], tag))
				test.add((tagEntry, OA["annotated"], Literal(item['AnnotationTime'])))
				test.add((review, RDF.type, OA["annotation"]))
				test.add((review,OA["hasBody"],Literal(str(item['Review']))))
				test.add((review,OA["hasTarget"],tagEntry))
				#test.add((review,OA["annotator"],reviewer))
				test.add((review,OA["annotated"],Literal(item['ReviewTime'])))
		sys.setdefaultencoding("utf-8")
		test.serialize(destination="test.rdf")
		train.serialize(destination="train.rdf")
	except:
		print sys.exc_info()
		g.close()



def split():
	train = rdflib.Graph()
	test = rdflib.Graph()
	g = rdflib.Graph()
	g.bind("oa","http://www.w3.org/ns/openannotation/core/")
	OA = Namespace("http://www.w3.org/ns/openannotation/core/")
	g.parse("tag.rdf")
	users = list(set([o for s,o in g.subject_objects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"))]))
	for user in users:
		print user
		annotations = [x for x in g.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotator"),user)]
		print len(annotations)
		sorted_annotations = sorted(annotations, key=lambda a: g.objects(a,(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/annotated"))))
		for i in range(0,min(10,len(annotations))):
			for p,o in g.predicate_objects(annotations[i]):
				train.add((annotations[i],p,o))
			review = g.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),annotations[i]).next()
			for s,p in g.subject_predicates(review):    
				train.add((s,p,review))

		if(len(annotations)>10):
			for i in range(10,len(annotations)):
				for p,o in g.predicate_objects(annotations[i]):
					test.add((annotations[i],p,o))
				review = g.subjects(rdflib.URIRef("http://www.w3.org/ns/openannotation/core/hasTarget"),annotations[i]).next()
				for s,p in g.subject_predicates():
					test.add((s,p,review))

	try:
		train.serialize(destination="train.rdf")
		test.serialize(destination="test.rdf")
	except:
		print sys.exc_info()
		train.close()
		
oa()
#split()
