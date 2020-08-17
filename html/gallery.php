<?php
$scale = $_GET["scale"];

$dir = __DIR__ . "/gallery";
$images = scandir($dir);
rsort($images);
$all ='"*"';

echo "<body><h1>Galerie</h1>\n";
echo "<p>Počet uložených snímků: " . (count($images) - 2) . "</p><br>\n";
echo "<label>Měřítko miniatur: </label>";
echo "<input id='scale' value='$scale'><br>\n";
echo "<button onclick='refresh()'>Aktualizovat</button><br>\n";
echo "<button onclick='rm($all)'>Smazat vše</button><br\n>";
echo "<hr><br>\n";

$width = 1920/$scale;
$height = 1080/$scale;

$server_name = $_SERVER["SERVER_NAME"];
foreach ($images as $img)
{
	if ($img != "." && $img != "..")
	{
		$rem = '"' . $img . '"';
		echo "<a href='http://$server_name/gallery/$img' target='_blank'>$img</a><br>\n";
		echo "<button onclick='rm($rem)'>Smazat</button><br>\n";
		echo "<img src='http://$server_name/gallery/$img' width='$width' height='$height'><br><br>\n";
	}
}

//script
echo "<script>\n".
"	function refresh() {\n".
"		var scale = document.getElementById('scale').value;".
"		window.location.href = 'http://$server_name/gallery.php?scale=' + scale;\n".
"	}\n".
"	\n".
"	function rm(img) {\n".
"		if (img == '*') {\n".
"			if (confirm('Fakt mam všechno smazat borče?')) {\n".
"				remove(img);".
"			}\n".
"		}\n".
"		else {\n".
"			if (confirm('Mám smazat ' + img + '? Vypadá fakt dobře :/')) {\n".
"				remove(img);".
"			}\n".
"		}\n".
"	}\n".
"	function remove(img) {\n".
"		var xmlhttp = new XMLHttpRequest();\n".
"		xmlhttp.onreadystatechange = function() {\n".
"			if (this.readyState == 4 && this.status == 200) {\n".
"				var response = this.responseText;\n".
"				console.log(response);\n".
"				refresh();\n".
"			}\n".
"		};\n".
"		xmlhttp.open('GET', 'remove.php?img=' + img);\n".
"		xmlhttp.send();\n".
"	}\n".
"</script></body>";
?>
