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
	testData       = testStruct{
		A: testInnerStruct{Name: "Andrew"},
		B: "tomi",
	}
)

type testInnerStruct struct {
	Name string `json:"name"`
}

type testStruct struct {
	A testInnerStruct `json:"a"`
	B string          `json:"b"`
}

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

func TestGetJSON(t *testing.T){
  var someData testStruct
  err := redisClient.GetJSON("user", &someData)
  if err != nil{
    t.Error(err)
  }
}

func TestSetJSON(t *testing.T) {
	err := redisClient.SetJSON("user", testData)
	if err != nil {
		t.Error(err)
	}
}
