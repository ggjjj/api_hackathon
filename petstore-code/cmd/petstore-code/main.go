package main

import (
	api "go-mod-name/internal/petstore-code"
)

func main() {

	api.NewAPIService().Start()
}
