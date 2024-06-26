<?php error_reporting(0);


function waf($s) {
        if (preg_match_all('/'. implode('|', array(
            '[' . preg_quote("(*<=>|'&-@") . ']',
            'select', 'and', 'or', 'if', 'by', 'from', 
            'where', 'as', 'is', 'in', 'not', 'having'
        )) . '/i', $s, $matches)) die(var_dump($matches[0]));
        return json_decode($s);
}

function funcion($sql) {
    
    $args = func_get_args();
    unset($args[0]);

    echo $args[1];

    echo vsprintf($sql, $args);

    $servername = "172.17.0.2";
    $username = "root";
    $password = "";
    $database = "dvwa";

    $conn = new mysqli($servername, $username, $password, $database);

    if ($conn -> connect_errno) {
        echo "Failed to connect to MySQL: " . $conn -> connect_error;
        exit();
    } 
        
        return $conn->query(vsprintf($sql, $args));
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $obj = waf(file_get_contents('php://input'));

    funcion("SELECT user, password FROM users WHERE user = '%s'", $obj->user);

} else {
    die(highlight_file(__FILE__, 1));
}

?>
