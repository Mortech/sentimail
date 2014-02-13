<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" type="text/css" href="email.css">
</head>
<body>

        
<?php
	
	$string = file_get_contents("../../backend/emailPos.json");
	$email=$_GET['email'];
	echo "<div id=\"name\">Emails from ".$email."</div>";
	echo"<div id=\"wrapper\">";
	$json_a=json_decode($string,true);
	
	for ($x=0; $x<=sizeof($json_a[$email]); $x++)
 	{
  		//echo $json_a[$email][$x][0] ."<br>";
  		//echo $json_a[$email][$x][1] ."<br>";
  		$subject="";
  		$garbage=true;
  		$polar="";
  		if($json_a[$email][$x][1]<0) $polar="negative";
  		else $polar="positive";
  		
  		echo sprintf("<div id=\"%s\"></div>",$polar);
  		//echo "<div id=\"negative\">1.00000000</div>";
  		echo sprintf("<div id=\"emailview%s\">",$polar);
  		$string = fopen(sprintf("../%s.",$json_a[$email][$x][0]),"r");
  		if ($string) {
			while (($line = fgets($string)) !== false ) {
				if($garbage)
				{
       					if(strlen($line) <= 2)
       					{
       						$garbage=false;	
       					}
       					if(strpos($line, "ubject:")==1)
       					{
       						$subject=$line;
       						echo $subject."<br>";
       					}
       				}
       				else
       				{
       					echo $line."<br>";
       				}
    			}
		} 
		else {
			echo "failed to open";
		}
  		echo "</div>";
  	} 	
?>      
</body>        