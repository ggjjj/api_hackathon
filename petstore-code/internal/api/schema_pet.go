package api

import (
	"fmt"
)

type Pet struct {
	Category	string	`json:"category"`
	Id	string	`json:"id"`
	Name	string	`json:"name"`
	Status	string	`json:"status"`
	Tags	[]string	`json:"tags"`
}

// Checks if all of the required fields for Pet are set
// and validates all of the constraints for the object.
func (obj *Pet) Validate() error {
	if obj == nil {
		return nil
	}
	fields := map[string]interface{}{
		"id": obj.Id,
		"name": obj.Name,
		"category": obj.Category,
		"status": obj.Status,
	}

	for field, value := range fields {
		if isEmpty := IsValEmpty(value); isEmpty{
			return fmt.Errorf("required field '%s' for object 'Pet' is empty or unset", field)
		}
	}

	allowedStatusValues := []interface{}{
		"available",
		"pending",
		"sold",
	}
	if !IsElemInEnum(obj.Status, allowedStatusValues) {
		return fmt.Errorf("field 'Status' in 'Pet' object is not one of the allowed values: '%v'", allowedStatusValues)
	}
	return nil
}

