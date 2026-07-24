<?php 

if (file_exists(__DIR__."/../matches.json")){
    $matches = json_decode((file_get_contents(__DIR__."/../matches.json")), true);
    return $matches;
}
else {
    return [];
}
?>