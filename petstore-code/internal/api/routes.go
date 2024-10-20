package api

import (
	"github.com/gorilla/mux"
	"net/http"
)


type Route struct {
	Name    string
	Path    string
	Method  string
	Handler http.HandlerFunc
}

type Routes []Route

func (h *APIHandler) AddRoutesToGorillaMux(router *mux.Router) {
	for _, route := range h.GetRoutes() {
		router.
			Name(route.Name).
			Path(route.Path).
			Methods(route.Method).
			Handler(route.Handler)
	}
}

func (h *APIHandler) GetRoutes() Routes {
	return Routes{
		{
			"getPets",
			"/pets",
			"GET",
			h.HandleGetPets,
		},{
			"addPet",
			"/pets",
			"POST",
			h.HandleAddPet,
		},{
			"deletePet",
			"/pets/{petId}",
			"DELETE",
			h.HandleDeletePet,
		},{
			"getPetById",
			"/pets/{petId}",
			"GET",
			h.HandleGetPetById,
		},{
			"updatePet",
			"/pets/{petId}",
			"PUT",
			h.HandleUpdatePet,
		},
	}
}

