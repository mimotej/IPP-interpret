<?php
$src_file;
$in_file;
$out_file;
$rc_file;
$jexam=FALSE;
$path=FALSE;
$parser_only=FALSE;
$interpreter_only=FALSE;
$recursive=FALSE;
$parser_file;
$header_done=false;
function getparams(){
    $longopts = array(
        "help",
        "directory:",
        "recursive",
        "parse-script:",
        "parse-only",
        "int-script:",
        "int-only",
        "jexamxml:",
    );
    $options = getopt("", $longopts);
    global $src_file;
    global $in_file;
    global $out_file;
    global $rc_file;
    global $jexam;
    global $path;
    global $parser_only;
    global $parser_file;
    global $interpreter_only;
    global $interpreter_file;
    global $recursive;
foreach ($options as $index => $value) {
    switch ($index) {
        case "help":
            echo "Testovací skript pro parser a interpret\n";
            exit(0);
        case "directory":
            $path = $value;
            break;
        case "recursive":
            $recursive = TRUE;
            break;
        case "parse-script":
            $parser_file = $value;
            break;
        case "int-script":
            $interpreter_file = $value;
            break;
        case "parse-only":
            if ($interpreter_only == TRUE) {
                exit(11);
            }
            $parser_only = TRUE;
            break;
        case "int-only":
            if ($parser_only == TRUE) {
                exit(11);
            }
            $interpreter_only = TRUE;
            break;
        case "jexamxml":
            $jexam = $value;
            break;
    }
}
}
function get_files($type, $array, $path){
    $output_array=array();
    global $recursive;
    $cdir=scandir($path);
    $a=0;
    foreach ($cdir as $entry) {
        if ($entry == ".." || $entry == ".") {
            continue;
        }
        if(is_dir($path."/".$entry) && $recursive == true) {
            $output_array=array_merge($output_array,get_files($type, $array, $path . "/" . $entry));
            $a=count($output_array);
        }
        if ($type === "src") {
            if (preg_match("/.*\.src/", $entry)) {
                $output_array[$a] = $path . "/" . $entry;
                $a++;
            }
        }
        elseif ($type === "out"){
            $length=count($array);
            for($i=0; $i < $length; $i++){
                $match=substr($array[$i], strpos($array[$i], "/"));
                $match=pathinfo($match, PATHINFO_FILENAME);
                $match .=".out";
                if($match === $entry){
                    $output_array[$i] = $path . "/" . $entry;
                }
            }
        }
        elseif ($type === "rc"){
            $length=count($array);
            for($i=0; $i < $length; $i++){
                $match=substr($array[$i], strpos($array[$i], "/"));
                $match=pathinfo($match, PATHINFO_FILENAME);
                $match .=".rc";
                if($match === $entry){
                    $output_array[$i] = $path . "/" . $entry;
                }
            }
        }
    }
    return $output_array;
}
getparams();
echo $path;
if($path == FALSE){
   $path=getcwd();
}
if($jexam == FALSE){
    $jexam="/pub/courses/ipp/jexamxml/jexamxml.jar";
}
if($parser_only == false && $interpreter_only==false){
    $src_array = get_files("src", "none", $path);
    $outfileshell;
    $outfileshellint;
    $result_interpret;
    $i = 0;
    $number_bad_files = 0;
    $e = 0;
    $result_parse = 5;
    $bad_file = "";
    $passed = 0;
    $d = 0;
    while ($i < count($src_array)) {
        $without_extension = substr_replace($src_array[$i], "", -4);
        $outfile = $without_extension . ".out";
        $rc_file = $without_extension . ".rc";
        $in_file = $without_extension . ".in";
        $exist = is_file($rc_file);
        if ($exist == false) {
            $rc_value=0;
        }
        if($exist== true) {
            $rc_value = file_get_contents($rc_file);
        }
        $exist=is_file($outfile);
        if($exist== false){
            $dump=fopen($outfile, "w");
        }
        $exist = is_file($in_file);
        if($exist == false){
            $dump=fopen($in_file, "w");
        }
        $command = "php " . $parser_file . " < " . $src_array[$i] . " > out.file";
        exec($command, $outfileshell, $result_parse);
        if($result_parse != 0) {
            if ($rc_value != $result_parse) {
                $bad_file .= "<tr><td>RC error - parser</td> <td>" . $without_extension . "</td></tr>";
                $number_bad_files++;
                $i++;
                continue;
            }
        }
        $command = "python3.8 " . $interpreter_file . " --source=" . "out.file" . " --input=" . $in_file . " > out1.file";
        exec($command, $outfileshellint, $result_interpret);
        $exist = is_file($outfile);
        if ($exist == false) {
            $outfile="";
        }
        if ($rc_value != $result_interpret) {
            $bad_file .= "<tr><td>RC error - Interpret</td> <td>" . $without_extension . "  [" . "ma byt -> ".$rc_value ." bylo -> " .$result_interpret. "]</td></tr>";
            $number_bad_files++;
            $i++;
            continue;
        }
        if ($rc_value != 0) {
            $passed++;
            $i++;
            continue;
        }
        $command = "diff out1.file " . $outfile;
        $outfileshell="";
        exec($command, $outfileshell, $result);
        if ($result == 0) {
            $passed++;
        } else {
            $bad_file .= "<tr><td>DIFF ERROR</td> <td>" . $without_extension . "</td><td>".implode("",$outfileshell)."</td</tr>";
            $number_bad_files++;
        }
        $i++;
    }
    $type = "Both";
    $output_html = "<HTML><BODY style=\"margin: 0 auto; width: 1280px;\"><H1>Vysledky testu</H1><H3>Typ testu: " . $type . "</H3>";
    $output_html .= "<table>" . "<tr><td>Proslo</td><td>Neproslo</td></tr><tr><td>" . $passed . "</td><td>" . $number_bad_files . "</td></tr></table>";
    $output_html .= "<H3>Chybne testy:</H3><table><tr><td>Typ chyby</td><td>Soubor</td></tr>" . $bad_file . "</table>";

}
if ($parser_only == true) {
    $src_array = get_files("src", "none", $path);
    $outfileshell;
    $result_interpret;
    $i = 0;
    $number_bad_files = 0;
    $e = 0;
    $result_parse = 5;
    $bad_file = "";
    $passed = 0;
    $d = 0;
    while ($i < count($src_array)) {
        $without_extension = substr_replace($src_array[$i], "", -4);
        $outfile = $without_extension . ".out";
        $rc_file = $without_extension . ".rc";
        if ($interpreter_only == false) {
            $command = "php7.4 " . $parser_file . " < " . $src_array[$i] . " > out.file";
            exec($command, $outfileshell, $result_parse);
        }
        $exist = is_file($outfile);
        if ($exist == false) {
            $i++;
            continue;
        }
        $exist = is_file($rc_file);
        if ($exist == false) {
            $i++;
            continue;
        }
        $rc_value = file_get_contents($rc_file);
        if ($rc_value != $result_parse) {
            $bad_file .= "<tr><td>RC error</td> <td>" . $without_extension . "</td></tr>";
            $number_bad_files++;
            $i++;
            continue;
        }
        if ($rc_value != 0) {
            $passed++;
            $i++;
            continue;
        }
        $command = "java -jar " . $jexam . " ./out.file " . "./" . $outfile;
        exec($command, $outfileshell, $result);
        if ($result_parse == 0) {   
            $passed++;
        } else {
            $bad_file .= "<tr><td>JEXAMXL error</td> <td>" . $without_extension . "</td></tr>";
            $number_bad_files++;
        }
        $i++;
    }
    if ($parser_only == true) {
        $type = "Parse";
    }
    $output_html = "<HTML><BODY style=\"margin: 0 auto; width: 1280px;\"><H1>Vysledky testu</H1><H3>Typ testu: " . $type . "</H3>";
    $output_html .= "<table>" . "<tr><td>Proslo</td><td>Neproslo</td></tr><tr><td>" . $passed . "</td><td>" . $number_bad_files . "</td></tr></table>";
    $output_html .= "<H3>Chybne testy:</H3><table><tr><td>Typ chyby</td><td>Soubor</td></tr>" . $bad_file . "</table>";
    $file_pointer="out1.file";
    unlink($file_pointer);
}
if ($interpreter_only == true) {
    $src_array = get_files("src", "none", $path);
    $outfileshell;
    $i = 0;
    $number_bad_files = 0;
    $e = 0;
    $result_parse = 5;
    $result_interpret;
    $bad_file = "";
    $passed = 0;
    $d = 0;
    $error_output="<TABLE><tr><td colspan='2'>DIFF ERROR-OUTPUTS</td></tr><tr><td>Soubor</td> <td>Výpis</td></tr>";
    $donotexist=0;
    while ($i < count($src_array)) {
        $without_extension = substr_replace($src_array[$i], "", -4);
        $outfile = $without_extension . ".out";
        $inputfile = $without_extension . ".in";
        $rc_file = $without_extension . ".rc";
        if(is_file($inputfile) != true){
            $inputfile="";
        }
        $command = "python3.8 " . $interpreter_file . " --source=" . $src_array[$i] . " --input=" . $inputfile . " > out.file";
        exec($command, $outfileshell, $result_interpret);
        $exist = is_file($outfile);
        if ($exist == false) {
            $i++;
            $passed++;
            continue;
        }
        $exist = is_file($rc_file);
        if ($exist == false) {
            $i++;
            $passed++;
            continue;
        }
        $rc_value = file_get_contents($rc_file);
        if ($rc_value != $result_interpret) {
            $bad_file .= "<tr><td>RC error</td> <td>" . $without_extension . "  [" . "má být -> ".$rc_value ." bylo -> " .$result_interpret. "]</td></tr>";
            $number_bad_files++;
            $i++;
            continue;
        }
        if ($rc_value != 0) {
            $passed++;
            $i++;
            continue;
        }
        $command = "diff out.file " . $outfile;
        exec($command, $outfileshell, $result);
        if ($result == 0) {
            $passed++;
        } else {
            $bad_file .= "<tr><td>DIFF ERROR</td> <td>" . $without_extension . "</td></tr>";
            $error_output .="<tr><td>".$without_extension."</td> <td>".implode("",$outfileshell)."</td></tr>";
            $number_bad_files++;
        }
        $i++;
    }
    if ($interpreter_only == true) {
        $type = "Interpreter";
    }
    $output_html = "<HTML><BODY style=\"margin: 0 auto; width: 1280px;\"><H1>Vysledky testu</H1><H3>Typ testu: " . $type . "</H3>";
    $output_html .= "<table>" . "<tr><td>Proslo</td><td>Neproslo</td></tr><tr><td>" . $passed . "</td><td>" . $number_bad_files . "</td></tr></table>";
    $output_html .= "<H3>Chybne testy:</H3><table><tr><td>Typ chyby</td><td>Soubor</td></tr>" . $bad_file . "</table>";
    $output_html.= $error_output."</TABLE>";
}
$file_pointer="out.file";
unlink($file_pointer);
$close_body="</BODY></HTML>";
$output_html.=$close_body;
echo($output_html);
echo "\n\n\n KONECNY VYSLEDEK:".$passed . "/".$i ;
?>