package server 

import "fmt"

type PostgresConnection struct {
	host     string
	port     string
	user     string
	password string
	database string
	debug    bool
}

func (this *PostgresConnection) GetConnectionName() string {
	return "postgres"
}

func (this *PostgresConnection) ConnectionString() string {
	// return DSN
	if this.debug {
		return fmt.Sprintf(
			"host=%v port=%v user=%v dbname=%v password=%v sslmode=disable TimeZone=Africa/Lagos",
			this.host, this.port, this.user, this.database, this.password)

	}
	return fmt.Sprintf(
		"host=%v port=%v user=%v dbname=%v password=%v sslmode=disable TimeZone=Africa/Lagos",
		this.host, this.port, this.user, this.database, this.password)
}
