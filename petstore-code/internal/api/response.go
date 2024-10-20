package api

import (
	"encoding/json"
	"encoding/xml"
	"fmt"
	"net/http"
	"reflect"
)

type Response struct {
	Code        int
	Body        interface{}
	Headers     map[string]string
	ContentType string
}

func NewResponse(code int, body interface{}, contentType string, headers map[string]string) Response {
	return Response{
		Code:        code,
		Body:        body,
		Headers:     headers,
		ContentType: contentType,
	}
}

// Sends a response back to the client with any included headers and attempty to properly encode the body
func (r *Response) Send(w http.ResponseWriter) error {
	// Set any response headers
	for header, headerVal := range r.Headers {
		w.Header().Set(header, headerVal)
	}

	// If there is no body to send, return early
	if r.Body == nil || (reflect.ValueOf(r.Body).Kind() == reflect.Ptr && reflect.ValueOf(r.Body).IsNil()) {
		return nil
	}

	// Try the following supported encodings
	var err error
	w.Header().Set("Content-Type", r.ContentType)
	switch r.ContentType {
	case "application/json":
		w.WriteHeader(r.Code)
		err = json.NewEncoder(w).Encode(r.Body)
	case "application/xml", "text/xml":
		w.WriteHeader(r.Code)
		err = xml.NewEncoder(w).Encode(r.Body)
	case "text/html", "text/plain":
		// Assume the body can be formatted as a string
		w.WriteHeader(r.Code)
		_, err = fmt.Fprintf(w, "%v", r.Body)
	case "application/octet-stream":
		w.WriteHeader(r.Code)
		if data, ok := r.Body.([]byte); ok {
			_, err = w.Write(data)
		} else {
			err = fmt.Errorf("unable to convert body to byte slice for application/octet-stream response")
		}
	}

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return fmt.Errorf("unable to write response body for content-type '%s', err: %w", r.ContentType, err)
	}

	return nil
}

// Sends a response back to the client with the provided code
// NOTE: this does not provide any reason to the client since
// some errors may contain sensitive information or reveal ways
// to exploit the server
func ErrorResponse(code int, w http.ResponseWriter) {
	w.WriteHeader(code)
}

// ErrorResponse represents the structure of the error response.
type ErrorMsg struct {
	Err string `json:"err"`
}

// Sends a response back to the client with the provided code and error message
func ErrorResponseWithMsg(code int, msg string, w http.ResponseWriter) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)

	errMsg := ErrorMsg{
		Err: msg,
	}

	json.NewEncoder(w).Encode(errMsg)
}
