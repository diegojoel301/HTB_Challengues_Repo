<?php
class Connection {
    private $dbHost = '172.17.0.2';
    private $dbUser = 'root';
    private $dbPass = '';
    private $dbName = 'dvwa';

    protected $conn;

    public function __construct() {
        $this->conn = new mysqli($this->dbHost, $this->dbUser, $this->dbPass, $this->dbName);

        if ($this->conn->connect_error) {
            die('Error de conexión a la base de datos: ' . $this->conn->connect_error);
        }
    }
}

?>
