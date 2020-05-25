package main

import (
	"context"
	"io"
	"log"
	"net/http"

	"github.com/gorilla/mux"

	firebase "firebase.google.com/go"
	"google.golang.org/api/option"
)

func main() {
	ctx := context.Background()
	sa := option.WithCredentialsFile("./serviceAccount.json")
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
	r.HandleFunc("/", YourHandler)
	r.HandleFunc("/live/last", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		last := last(client, ctx)
		io.WriteString(w, last)
	})
	r.HandleFunc("/live/upcoming", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		up := upcome(client, ctx)
		io.WriteString(w, up)
	})
	r.HandleFunc("/live/now", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		now := live(client, ctx)
		io.WriteString(w, now)
	})

	// Bind to a port and pass our router in
	log.Fatal(http.ListenAndServe(":8000", r))
}

func YourHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Humanz Api\n"))
}
