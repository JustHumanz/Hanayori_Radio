//Engine
package main

import (
	"encoding/json"
	"log"

	"cloud.google.com/go/firestore"
	"google.golang.org/api/iterator"
)

//struct for convert map to json
type VtubeData struct {
	Data map[string]interface{} `json:"Data"`
}

func exec(iter *firestore.DocumentIterator) string {
	var tmp []VtubeData
	for {
		doc, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		tmp = append(tmp, VtubeData{Data: doc.Data()})
	}

	jso, err := json.Marshal(tmp)
	if err != nil {
		log.Fatal(err)
	}
	return (string(jso))
}

func query(client *firestore.Client, q *firestore.DocumentIterator) string {
	fix := exec(q)
	return (fix)
}
