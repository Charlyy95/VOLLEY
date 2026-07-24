<?php require_once (__DIR__."/script/recup_matches.php") ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mes matchs</title>
    <link href="CSS/my_matches.css" rel="stylesheet">
    <link href="CSS/root.css" rel="stylesheet">

    <!--<link rel="icon" href="img/logo.png">      icone dans l'onglet du navigateur-->

</head>

<body>
    <div class="matches_area">
        <h2> MES MATCHS </h2>

        <div class="matches_list">

        <?php 
        $count = 0; 
        foreach ($matches as $match): ?>
            
            <div class="match_container"> <h3> MATCH <?= ($count +1) ?> </h3>
                <div class="detail_match">

                    <div class="params"><img src="img/calendar.png" alt="date" class="icon"> <?= $matches[$count]["date"] ?></div>
                    <div class="params"><img src="img/clock.png" alt="hour" class="icon"> <?= $matches[$count]["heure"] ?> </div>
                    <div class="params"><img src="img/loc.png" alt="place" class="icon"> <?= $matches[$count]["salle"] ?> </div>
                    <?php
                    if ($matches[$count]["domicile"] == "SOCIETE VB FRANCONVILLE") { ?>
                        <div class="params"><img src="img/duel.png" alt="opponent" class="icon"> <?= $matches[$count]["exterieur"] ?> </div>

                    <?php }

                    else { ?>
                        <div class="params"><img src="img/duel.png" alt="opponent" class="icon"> <?= $matches[$count]["domicile"] ?> </div>

                    <?php } ?>
                </div>
            </div>
        <?
        $count ++;
        endforeach ?>
        </div>        

    </div>

</body>

</html>