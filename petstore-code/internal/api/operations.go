package api

import (
	"context"
	"github.com/rs/zerolog"
	"net/http"
	"os"
	"time"
)


// APIHandler is a type to give the api functions below access to a common logger
// any any other shared objects
type APIHandler struct {
	// Zerolog was chosen as the default logger, but you can replace it with any logger of your choice
	logger zerolog.Logger

	// Note: if you need to pass in a client for your database, this would be a good place to include it
}

func NewAPIHandler() *APIHandler {
	output := zerolog.ConsoleWriter{Out: os.Stderr, TimeFormat: time.RFC3339}
	logger := zerolog.New(output).With().Timestamp().Logger()
	return &APIHandler{logger: logger}
}

func (h *APIHandler) WithLogger(logger zerolog.Logger) *APIHandler {
	h.logger = logger
	return h
}

// Adds a new pet to the inventory.
// Add a new pet
func (h *APIHandler) AddPet(ctx context.Context, reqBody Pet) (Response, error) {
	// TODO: implement the AddPet function to return the following responses

	// return NewResponse(201, Pet{}, "application/json", responseHeaders), nil

	// return NewResponse(400, {}, "", responseHeaders), nil

	// return NewResponse(500, {}, "", responseHeaders), nil

	return NewResponse(http.StatusNotImplemented, ErrorMsg{"addPet operation has not been implemented yet"}, "application/json", nil), nil
}

// Removes a pet from the inventory.
// Delete a pet
func (h *APIHandler) DeletePet(ctx context.Context, petId string) (Response, error) {
	// TODO: implement the DeletePet function to return the following responses

	// return NewResponse(204, {}, "", responseHeaders), nil

	// return NewResponse(404, {}, "", responseHeaders), nil

	// return NewResponse(500, {}, "", responseHeaders), nil

	return NewResponse(http.StatusNotImplemented, ErrorMsg{"deletePet operation has not been implemented yet"}, "application/json", nil), nil
}

// Fetches a single pet by its ID.
// Retrieve a pet by ID
func (h *APIHandler) GetPetById(ctx context.Context, petId string) (Response, error) {
	// TODO: implement the GetPetById function to return the following responses

	// return NewResponse(200, Pet{}, "application/json", responseHeaders), nil

	// return NewResponse(404, {}, "", responseHeaders), nil

	// return NewResponse(500, {}, "", responseHeaders), nil

	return NewResponse(http.StatusNotImplemented, ErrorMsg{"getPetById operation has not been implemented yet"}, "application/json", nil), nil
}

// Fetches a list of all pets available in the inventory.
// Retrieve a list of pets
func (h *APIHandler) GetPets(ctx context.Context) (Response, error) {
	// TODO: implement the GetPets function to return the following responses

	// return NewResponse(200, []Pet, "application/json", responseHeaders), nil

	// return NewResponse(404, {}, "", responseHeaders), nil

	// return NewResponse(500, {}, "", responseHeaders), nil

	return NewResponse(http.StatusNotImplemented, ErrorMsg{"getPets operation has not been implemented yet"}, "application/json", nil), nil
}

// Updates the details of an existing pet.
// Update an existing pet
func (h *APIHandler) UpdatePet(ctx context.Context, petId string, reqBody Pet) (Response, error) {
	// TODO: implement the UpdatePet function to return the following responses

	// return NewResponse(200, Pet{}, "application/json", responseHeaders), nil

	// return NewResponse(400, {}, "", responseHeaders), nil

	// return NewResponse(404, {}, "", responseHeaders), nil

	// return NewResponse(500, {}, "", responseHeaders), nil

	return NewResponse(http.StatusNotImplemented, ErrorMsg{"updatePet operation has not been implemented yet"}, "application/json", nil), nil
}

