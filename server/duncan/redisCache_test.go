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
)

func TestInvalidConnection(t *testing.T) {
	os.Stdout, _ = os.Open(os.DevNull)
	_, err := NewRedisclient(invalid_connection)
	if err == nil {
		t.Error("Testing invalid connection failed")
	}
}

func TestValidConnection(t *testing.T) {
	os.Stdout, _ = os.Open(os.DevNull)
	_, err := NewRedisclient(valid_connection)
	if err != nil {
		t.Error("Testing valid connection failed")
	}
}
