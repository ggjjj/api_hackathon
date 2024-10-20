package api

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

// HandleAddPet handles parsing input to pass to the AddPet operation and sends responses back to the client
func (h *APIHandler) HandleAddPet(w http.ResponseWriter, r *http.Request) {
	var err error
	reqBody := Pet{}
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&reqBody); err != nil {
		ErrorResponseWithMsg(http.StatusBadRequest, "request body was not able to be parsed successfully 'Pet'", w)
		return
	}
	if err := reqBody.Validate(); err != nil {
		errMsg := fmt.Errorf("request body was parsed successfully but failed validation, err: %w", err)
		ErrorResponseWithMsg(http.StatusBadRequest, errMsg.Error(), w)
		return
	}

	response, err := h.AddPet(r.Context(), reqBody)
	if err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("AddPet returned err: %s", err)
	}

	if err = response.Send(w); err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("AddPet was unable to send it's response, err: %s", err)
	}
}

// HandleDeletePet handles parsing input to pass to the DeletePet operation and sends responses back to the client
func (h *APIHandler) HandleDeletePet(w http.ResponseWriter, r *http.Request) {
	var err error
	pathParams := mux.Vars(r)

	var petId string
	petId = pathParams["petId"]
	if petId == ""{
		ErrorResponseWithMsg(http.StatusBadRequest, "request is missing required path parameter 'petId'", w)
		return
	}

	response, err := h.DeletePet(r.Context(), petId)
	if err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("DeletePet returned err: %s", err)
	}

	if err = response.Send(w); err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("DeletePet was unable to send it's response, err: %s", err)
	}
}

// HandleGetPetById handles parsing input to pass to the GetPetById operation and sends responses back to the client
func (h *APIHandler) HandleGetPetById(w http.ResponseWriter, r *http.Request) {
	var err error
	pathParams := mux.Vars(r)

	var petId string
	petId = pathParams["petId"]
	if petId == ""{
		ErrorResponseWithMsg(http.StatusBadRequest, "request is missing required path parameter 'petId'", w)
		return
	}

	response, err := h.GetPetById(r.Context(), petId)
	if err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("GetPetById returned err: %s", err)
	}

	if err = response.Send(w); err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("GetPetById was unable to send it's response, err: %s", err)
	}
}

// HandleGetPets handles parsing input to pass to the GetPets operation and sends responses back to the client
func (h *APIHandler) HandleGetPets(w http.ResponseWriter, r *http.Request) {
	var err error
	response, err := h.GetPets(r.Context())
	if err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("GetPets returned err: %s", err)
	}

	if err = response.Send(w); err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("GetPets was unable to send it's response, err: %s", err)
	}
}

// HandleUpdatePet handles parsing input to pass to the UpdatePet operation and sends responses back to the client
func (h *APIHandler) HandleUpdatePet(w http.ResponseWriter, r *http.Request) {
	var err error
	pathParams := mux.Vars(r)

	var petId string
	petId = pathParams["petId"]
	if petId == ""{
		ErrorResponseWithMsg(http.StatusBadRequest, "request is missing required path parameter 'petId'", w)
		return
	}

	reqBody := Pet{}
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&reqBody); err != nil {
		ErrorResponseWithMsg(http.StatusBadRequest, "request body was not able to be parsed successfully 'Pet'", w)
		return
	}
	if err := reqBody.Validate(); err != nil {
		errMsg := fmt.Errorf("request body was parsed successfully but failed validation, err: %w", err)
		ErrorResponseWithMsg(http.StatusBadRequest, errMsg.Error(), w)
		return
	}

	response, err := h.UpdatePet(r.Context(), petId, reqBody)
	if err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("UpdatePet returned err: %s", err)
	}

	if err = response.Send(w); err != nil {
		ErrorResponse(http.StatusInternalServerError, w)
		h.logger.Error().Msgf("UpdatePet was unable to send it's response, err: %s", err)
	}
}

