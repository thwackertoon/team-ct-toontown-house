<?php

function fgetcont($filepath) {
    $f = fopen($filepath,"rb");
    $size = filesize($filepath);
    $data = fread($f,$size);
    fclose($f);
    return $data;
}

function fputcont($filepath,$data) {
    $f = fopen($filepath,"rb");
    fwrite($f,$data);
    fclose($f);
}

function gzdecode($data) 
{ 
   return zlib_decode(substr($data,10,-8)); 
} 
class Blob {
    	function __construct($file) {		$data = fgetcont($file);		if ($data) {
            $data = gzdecode($data);
            $chr1 = chr(1);
            $data = explode($chr1,$data);
        }
        
        else $data=array();                $this->origFile = $file;
        $this->files = array();
        
        if (count($data) >= 2) {
        
            $_range = range(0,count($data),2);            foreach ($_range as $i) {                $this->files[$data[$i]] = base64_decode($data[$i+1]);            }
            
        }                unset($data);    }        function bake() {        $o='';        foreach($this->files as $file) {            $o += chr(1);            $o += $file;            $o += chr(1);            $o += base64_encode($this->files[file]);        }        return zlib_encode($o);      }        function read($file) {        if (!in_array($file,$this->files)) return "";        return $this->files[$file];    }        function write($file,$data,$append = true) {        if (!in_array($file,$this->files)) {             $this->files[$file]=$data;            return;        }        if (append) $this->files[$file]+=$data;        else $this->files[$file]=$data;    }                function exists($file) {        return (in_array($file,$this->files));    }        function flushBlob() {        fputcont($this->origFile,$this->bake());    }                function all() {        return $this->files;    }}
?>