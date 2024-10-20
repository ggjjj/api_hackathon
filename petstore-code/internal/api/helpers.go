package api

import (
	"encoding/json"
	"fmt"
	"reflect"
	"strconv"
	"strings"
)

// IsValEmpty checks if the provided value is empty or not
func IsValEmpty(val interface{}) bool {
	if val == nil {
		return true
	}
	return reflect.DeepEqual(val,
		reflect.Zero(reflect.TypeOf(val)).Interface(),
	)
}

// IsElemInEnum returns true when the elem is a member of the provided enum
// Supports various types such as ints, objects, arrays, etc.
func IsElemInEnum(elem interface{}, enum []interface{}) bool {
	elemVal := reflect.ValueOf(elem)
	for _, e := range enum {
		if reflect.DeepEqual(elemVal.Interface(), reflect.ValueOf(e).Interface()) {
			return true
		}
	}
	return false
}

// IsMultipleOf checks if num is a multiple of factor.
// Both num and factor can be any of int, int32, int64, float32, float64.
// Returns true if num is a multiple of factor, false otherwise.
func IsMultipleOf(num interface{}, factor interface{}) (bool, error) {
	numFloat, ok := toFloat64(num)
	if !ok {
		return false, fmt.Errorf("unable to perform multipleOf check, num '%v' is not a numeric type", num)
	}

	factorFloat, ok := toFloat64(factor)
	if !ok {
		return false, fmt.Errorf("unable to perform multipleOf check, factor '%v' is not a numeric type", factor)
	}

	if factorFloat == 0 {
		return false, fmt.Errorf("unable to perform multipleOf check, factor cannot be zero")
	}

	// Using modulo operation to check for multiple.
	// For floating-point numbers, consider the result a multiple if the remainder is very small (to handle precision issues).
	remainder := numFloat / factorFloat
	remainderInt := int(remainder)
	isMultiple := remainder-float64(remainderInt) == 0

	return isMultiple, nil
}

// toFloat64 attempts to convert an interface{} to float64.
func toFloat64(val interface{}) (float64, bool) {
	switch v := val.(type) {
	case int:
		return float64(v), true
	case int32:
		return float64(v), true
	case int64:
		return float64(v), true
	case float32:
		return float64(v), true
	case float64:
		return v, true
	default:
		return 0, false
	}
}

// Parse an input string as an int
func ParseInt(str string) (int, error) {
	if str == "" {
		return 0, nil
	}

	return strconv.Atoi(str)
}

// Parse an input string as an int32
func ParseInt32(str string) (int32, error) {
	if str == "" {
		return 0, nil
	}

	val, err := strconv.ParseInt(str, 10, 32)
	if err != nil {
		return 0, err
	}

	return int32(val), nil
}

// Parse an input string as an int64
func ParseInt64(str string) (int64, error) {
	if str == "" {
		return 0, nil
	}

	return strconv.ParseInt(str, 10, 64)
}

// Parse an input string as a float32
func ParseFloat32(str string) (float32, error) {
	if str == "" {
		return 0.0, nil
	}

	val, err := strconv.ParseFloat(str, 32)
	if err != nil {
		return 0.0, err
	}

	return float32(val), nil
}

// Parse an input string as a float64
func ParseFloat64(str string) (float64, error) {
	if str == "" {
		return 0.0, nil
	}

	return strconv.ParseFloat(str, 64)
}

// Parse an input string as a bool
func ParseBool(str string) (bool, error) {
	if str == "" {
		return false, nil
	}

	return strconv.ParseBool(str)
}

// Takes an input string ant attempts to parse it as the given object
func ParseObjectFromJSON[T any](input string) (T, error) {
	var result T
	err := json.Unmarshal([]byte(input), &result)
	if err != nil {
		return result, err
	}
	return result, nil
}

// Takes an input string ant attempts to parse it as a slice of the given object
func ParseSliceFromJSON[T any](input string) ([]T, error) {
	// Correcting input format to make it a valid JSON array
	input = strings.TrimSpace(input)
	if strings.HasPrefix(input, "{[") && strings.HasSuffix(input, "]}") {
		input = "[" + input[2:len(input)-1] + "]"
	}

	var result []T
	err := json.Unmarshal([]byte(input), &result)
	if err != nil {
		return nil, err
	}
	return result, nil
}
