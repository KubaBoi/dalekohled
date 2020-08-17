<?php
$file = fopen("settings.txt", "r");
$settVal = explode('|', fread($file, filesize("settings.txt")));
fclose($file);

echo "<h1>Ovládání teleskopu</h1>\n";

echo "<a href='http://" . $_SERVER["SERVER_NAME"] . ":8000' target='_blank'>Kamera</a>\n";
echo "<a href='gallery.php?scale=3' target='_blank'>Galerie</a><br><br>\n";

$script = '"takePic.php"';
echo "<button onclick='callPHP($script)'>Snímek</button>\n";
echo "<button onclick='changeSettings(1)'>Aktualizovat nastavení</button><br>\n";
echo "<label id='newPhoto'></label><br>\n";

echo "<select id='f'>\n".
"	<option value='20'>20 mm</option>\n".
"	<option value='12,5'>12.5 mm</option>\n".
"	<option value='4'>4 mm</option>\n".
"</select><br>\n";

echo "<table><tr>\n";
echo "	<td>Rozlišení X (max 2592):</td>\n";
echo "	<td><input id='resX' value='$settVal[0]'></input></td>\n";
echo "</tr>\n";

echo "<tr>\n";
echo "	<td>Rozlišení Y (max 1944):</td>\n";
echo "	<td><input id='resY' value='$settVal[1]'></input></td>\n";
echo "</tr>\n";

echo "<tr>\n";
echo "	<td>Framerate (max 15):</td>\n";
echo "	<td><input id='fps' type='number' min='1' max='15' value='$settVal[2]'></input></td>\n";
echo "</tr>\n";

echo "<tr>\n";
echo "	<td>Anotace:</td>\n";
echo "	<td><input id='anot' value='$settVal[3]'></input></td>\n";
echo "</tr>\n";

echo "<tr>\n";
echo "	<td>Brightness (0-100):</td>\n";
echo "	<td><input id='bright' type='number' min='0' max='100' value='$settVal[4]'></input></td>\n";
echo "</tr>\n";

echo "<tr>\n";
echo "	<td>Contrast (0-100):</td>\n";
echo "	<td><input id='contr' type='number' min='0' max='100' value='$settVal[5]'></input></td>\n";
echo "</tr>\n";

echo "<tr>\n";
echo "	<td>Exposure mode:</td>\n";
echo "	<td><select id='exposMode'>".
"		<option value='$settVal[6]' selected disabled hidden>$settVal[6]</option>".
"		<option value='auto'>auto</option>".
"		<option value='off'>off</option>".
"		<option value='night'>night</option>".
"		<option value='nightpreview'>nightpreview</option>".
"		<option value='backlight'>backlight</option>".
"		<option value='spotlight'>spotlight</option>".
"		<option value='sports'>sports</option>".
"		<option value='snow'>snow</option>".
"		<option value='beach'>beach</option>".
"		<option value='verylong'>verylong</option>".
"		<option value='fixedfps'>fixedfps</option>".
"		<option value='antishake'>antishake</option>".
"		<option value='fireworks'>fireworks</option>".
"	</select></td>\n";
echo "</tr>\n";

echo "<tr>\n";
echo "	<td>AWB mode:</td>\n";
echo "	<td><select id='awbMode'>".
"		<option value='$settVal[7]' selected disabled hidden>$settVal[7]</option>".
"		<option value='auto'>auto</option>".
"		<option value='off'>off</option>".
"		<option value='sunlight'>sunlight</option>".
"		<option value='cloudy'>cloudy</option>".
"		<option value='shade'>shade</option>".
"		<option value='tungsten'>tungsten</option>".
"		<option value='fluorescent'>fluorescent</option>".
"		<option value='incandescent'>incandescent</option>".
"		<option value='flash'>flash</option>".
"		<option value='horizon'>horizon</option>".
"	</select></td>\n";
echo "</tr></table>\n";

echo "<img width='640' height='360' id='photo'>\n";

echo "<div style='float:  right'>\n".
"	<img id='stream' width='640' height='360' src='offStream.png'><br><br>\n".
"	<button id='onOff' onclick='onOff()'>Zapnout</button>\n".
"	<button onclick='changeFps()'>Změnit Framerate</button>\n".
"</div>\n";

//script
echo "<script>\n".
"	var v;\n".
"	function callPHP(script) {\n".
"		changeSettings(0);\n".
"		var xmlhttp = new XMLHttpRequest();\n".
"		xmlhttp.onreadystatechange = function() {\n".
"			if (this.readyState == 4 && this.status == 200) {\n".
"				var response = this.responseText;\n".
"				console.log(response);\n".
"				if (script == 'takePic.php?f=' + document.getElementById('f').value) {\n".
"					document.getElementById('newPhoto').innerHTML = response;\n".
"					v = setTimeout(waitForPicture, 8000, 'gallery/' + response);\n".
"				}\n".
"			}\n".
"		};".
"		if (script == 'takePic.php') {\n".
"			script += '?f=' + document.getElementById('f').value;\n".
"		}\n".
"		xmlhttp.open('GET', script, true);\n".
"		xmlhttp.send();\n".
"	}\n".
"	function waitForPicture(img) {\n".
"		document.getElementById('photo').src = img;\n".
"	}\n".
"\n".
"	function onOff() {\n".
"		if (document.getElementById('onOff').innerHTML == 'Vypnout') {\n". //vypnout stream
"			document.getElementById('stream').src = 'offStream.png';\n".
"			document.getElementById('onOff').innerHTML = 'Zapnout';\n".
"		}\n".
"		else {\n". //zapnout stream
"			document.getElementById('stream').src = 'http://" . $_SERVER["SERVER_NAME"] . ":8000/stream.mjpg';\n".
"			document.getElementById('onOff').innerHTML = 'Vypnout';\n".
"		}\n".
"	}\n".
"\n".
"	function changeFps() {\n".
"		var xmlhttp = new XMLHttpRequest();\n".
"		xmlhttp.onreadystatechange = function() {\n".
"			if (this.readyState == 4 && this.status == 200) {\n".
"				var response = this.responseText;\n".
"				console.log(response);\n".
"			}\n".
"		};\n".
"		xmlhttp.open('GET', 'changeFps.php', true);\n".
"		xmlhttp.send();\n".
"	}\n".
"\n".
"	function changeSettings(picture) {\n".
"		var xmlhttp = new XMLHttpRequest();\n".
"		xmlhttp.onreadystatechange = function() {\n".
"			if (this.readyState == 4 && this.status == 200) {\n".
"				var response = this.responseText;\n".
"				console.log(response);\n".
"			}\n".
"		};\n".
"		var values = '';\n".
"		values += document.getElementById('resX').value + '|';\n".
"		values += document.getElementById('resY').value + '|';\n".
"		values += document.getElementById('fps').value + '|';\n".
"		values += document.getElementById('anot').value + '|';\n".
"		values += document.getElementById('bright').value + '|';\n".
"		values += document.getElementById('contr').value + '|';\n".
"		values += document.getElementById('exposMode').value + '|';\n".
"		values += document.getElementById('awbMode').value + '|';\n".
"		xmlhttp.open('GET', 'changeSettings.php?values=' + values + '&pic=' + picture, true);\n".
"		xmlhttp.send();\n".
"	}\n".
"</script>";
?>
