package main

import (
	"context"
	"io"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"

	"cloud.google.com/go/firestore"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"

	firebase "firebase.google.com/go"
	"google.golang.org/api/option"
)

func main() {
	//Auth firestore project
	ctx := context.Background()
	sa := option.WithCredentialsFile("./serviceAccount.json") //change with your config
	app, err := firebase.NewApp(ctx, nil, sa)
	if err != nil {
		log.Fatalln(err)
	}

	client, err := app.Firestore(ctx)
	if err != nil {
		log.Fatalln(err)
	}
	defer client.Close()

	r := mux.NewRouter()
	// Routes consist of a path and a handler function.
	r.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Humanz Api\n"))
	})

	//get last live from firestore
	r.HandleFunc("/live/last", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		//query in firestore
		q := client.Collection("video").Where("status", "in", []string{"past", "uploaded"}).OrderBy("publishedAt", firestore.Desc).Documents(ctx)
		last := query(client, q)
		io.WriteString(w, last)
	})

	//get last live from every member
	r.HandleFunc("/live/last/{member}", func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		member := strings.ToLower(vars["member"])

		var q *firestore.DocumentIterator
		//query in firestore
		if member == "kano" {
			q = client.Collection("video").Where("status", "in", []string{"past", "uploaded"}).Where("ytChannelId", "==", "UCfuz6xYbYFGsWWBi3SpJI1w").OrderBy("publishedAt", firestore.Desc).Documents(ctx)
		} else if member == "hitona" {
			q = client.Collection("video").Where("status", "in", []string{"past", "uploaded"}).Where("ytChannelId", "==", "UCV2m2UifDGr3ebjSnDv5rUA").OrderBy("publishedAt", firestore.Desc).Documents(ctx)
		} else if member == "hareru" || member == "parerun" {
			q = client.Collection("video").Where("status", "in", []string{"past", "uploaded"}).Where("ytChannelId", "==", "UCyIcOCH-VWaRKH9IkR8hz7Q").OrderBy("publishedAt", firestore.Desc).Documents(ctx)
		} else if member == "nonono" {
			q = client.Collection("video").Where("status", "in", []string{"past", "uploaded"}).Where("ytChannelId", "==", "UCiexEBp7-D46FXUtQ-BpgWg").OrderBy("publishedAt", firestore.Desc).Documents(ctx)
		} else {
			return
		}
		last := query(client, q)
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		io.WriteString(w, last)
	})

	//get upcome live
	r.HandleFunc("/live/upcoming", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		//query in firestore
		q := client.Collection("video").Where("status", "in", []string{"live", "upcoming"}).Where("liveViewers", "==", nil).OrderBy("publishedAt", firestore.Desc).Documents(ctx)
		up := query(client, q)
		io.WriteString(w, up)
	})
	//get live now
	r.HandleFunc("/live/now", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		//query in firestore
		q := client.Collection("video").Where("status", "==", "live").Where("liveViewers", ">", "").OrderBy("liveViewers", firestore.Desc).OrderBy("publishedAt", firestore.Desc).Documents(ctx)
		now := query(client, q)
		io.WriteString(w, now)
	})
	r.HandleFunc("/twitter/{member}", twitter)
	r.HandleFunc("/twitter/{member}/{limit}", twitter)

	// Bind to a port and pass our router in
	loggedRouter := handlers.LoggingHandler(os.Stdout, r)
	log.Println("listening on 8000")
	http.ListenAndServe(":8000", loggedRouter)
}

func twitter(w http.ResponseWriter, r *http.Request) {
	var last string
	vars := mux.Vars(r)
	member := strings.ToLower(vars["member"])
	limit := strings.ToLower(vars["limit"])

	if limit == "" {
		limit = "10"
	} else if limit == "all" {
		limit = "1337"
	} else if matched, _ := regexp.MatchString(`^[0-9]*$`, limit); matched == false {
		w.WriteHeader(http.StatusNotFound)
		return
	}

	if member == "kano" {
		last = tw("#鹿乃art -filter:retweets filter:media", limit)
	} else if member == "hitona" {
		last = tw("#ひとなーと -filter:retweets filter:media", limit)
	} else if member == "hareru" || member == "parerun" {
		last = tw("#はなまるお絵かき -filter:retweets filter:media", limit)
	} else if member == "nonono" {
		last = tw("#ののののえ -filter:retweets filter:media", limit)
	} else if member == "all" {
		last = tw("#鹿乃art OR #ひとなーと OR #はなまるお絵かき OR #ののののえ -filter:retweets filter:media", limit)
	} else {
		w.WriteHeader(http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	io.WriteString(w, last)
}
