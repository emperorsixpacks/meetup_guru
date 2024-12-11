package duncan

import (
	"os"
	"testing"
)

var (
	invalid_connection = RedisConnetion{
		Addr:     "localhost:6378",
		Password: "",
		DB:       1,
	}
	valid_connection = RedisConnetion{
		Addr:     "localhost:6379",
		Password: "",
		DB:       1,
	}
	redisClient, _ = NewRedisclient(valid_connection)
)

func TestInvalidConnection(t *testing.T) {
  os.Stdout, _ = os.Open(os.DevNull)
	_, err := NewRedisclient(invalid_connection)
	if err == nil {
		t.Error("Testing invalid connection failed")
	}
}

func TestValidConnection(t *testing.T) {
	_, err := NewRedisclient(valid_connection)
	if err != nil {
		t.Error("Testing valid connection failed")
	}
}

func TestRestoretDB(t *testing.T) {
	type TestInnerStruct struct {
		Name string `json:"name"`
	}

	type TestStruct struct {
		A TestInnerStruct `json:"a"`
		B string          `json:"b"`
	}
	testData := TestStruct{
		A: TestInnerStruct{Name: "Andrew"},
		B: "tomi",
	}
	err := redisClient.SetJSON("user", testData)
	if err != nil {
    t.Error(err)
	}
  // from what i can see, from test, the data is not geting modofied in db
}

