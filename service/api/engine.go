//Engine
package main

import (
	"encoding/json"
	"log"
	"strconv"

	"cloud.google.com/go/firestore"
	twitterscraper "github.com/JustHumanz/twitter-scraper"
	"google.golang.org/api/iterator"
)

func exec(iter *firestore.DocumentIterator) string {
	var tmp []interface{}
	for {
		doc, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		tmp = append(tmp, doc.Data())
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

func tw(tag string, limit string) string {
	var tmp []twitterscraper.Tweet
	count, err := strconv.Atoi(limit)

	if err != nil {
		log.Panic(err)
	}

	for tweet := range twitterscraper.SearchTweets(tag, count) {
		if tweet.Error != nil {
			panic(tweet.Error)
		}
		tmp = append(tmp, tweet.Tweet)
	}
	result, err := json.Marshal(tmp)
	if err != nil {
		log.Println(err)
	}
	return (string(result))
}
