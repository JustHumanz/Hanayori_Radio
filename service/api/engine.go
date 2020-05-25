package main

import (
	"context"
	"encoding/json"
	"log"

	"cloud.google.com/go/firestore"
	"google.golang.org/api/iterator"
)

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
		tmp = append(tmp, VtubeData{Data: doc.Data()})
	}
	jso, err := json.Marshal(tmp)
	if err != nil {
		log.Fatal(err)
	}
	return (string(jso))
}

//get live data
func live(client *firestore.Client, ctx context.Context) string {
	q := client.Collection("video").Where("status", "==", "live").Where("liveViewers", ">", "").OrderBy("liveViewers", firestore.Desc).OrderBy("publishedAt", firestore.Desc).Documents(ctx)
	fix := exec(q)
	return (fix)
}

//get upcome data
func upcome(client *firestore.Client, ctx context.Context) string {
	q := client.Collection("video").Where("status", "in", []string{"live", "upcoming"}).Where("liveViewers", "==", nil).OrderBy("publishedAt", firestore.Desc).Documents(ctx)
	fix := exec(q)
	return (fix)
}

//get last stream data
func last(client *firestore.Client, ctx context.Context) string {
	q := client.Collection("video").Where("status", "in", []string{"past", "uploaded"}).OrderBy("publishedAt", firestore.Desc).Documents(ctx)
	fix := exec(q)
	return (fix)
}
