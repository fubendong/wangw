<?php

//http://gw.api.taobao.com/router/rest?app_key=21600714
//&buyer_nick=zgl9520
//&format=json
//&group_ids=306536820
//&method=taobao.crm.members.group.add
//&session=630271959240d177d340a8b310c8e3ZZd9fc57e8ed821e3634775402
//&sign=AA4D04F7EC3DD39F2D188A22CE928117
//&sign_method=md5
//&timestamp=1410439723173
//&v=2.0
$arr = array(
	"app_key" =>"23018966",
	"buyer_nick" =>"18671686530l",
	"format" =>"json",
	"group_ids" =>"306568907",
	"method" =>"taobao.crm.members.group.add",
	"session" =>"6302b157320d31a35ee65c2799ZZ53409ac089c542687f0634775402",
	"sign_method" =>"md5",
	"timestamp" =>"1410443760765",
	"v" =>"2.0"
);

$new_arr = ksort($arr);

var_dump($arr);
$str = '';
foreach($arr as $key => $value){
	
	$str .= $key.$value;
	
}
$str = "e8792cf243614eb3c7c16b8c05d6135a".$str."e8792cf243614eb3c7c16b8c05d6135a";

var_dump($str);
$md5 = strtoupper(md5($str));
var_dump($str);
var_dump($md5);


//
//http://gw.api.taobao.com/router/rest?app_key=23018966&buyer_nick=18671686530l&format=json&group_ids=306568907&method=taobao.crm.members.group.add&session=6302b157320d31a35ee65c2799ZZ53409ac089c542687f0634775402&sign=45784CBE4F5448FA61AC2F1DBE62558B&sign_method=md5&timestamp=1410443760765&v=2.0
//
//
//http://gw.api.taobao.com/router/rest?
//app_key=21600714
//&buyer_nick=ngpllyyqx5477
//&format=json&group_ids=306568907
//&method=taobao.crm.members.group.add
//&session=6302b157320d31a35ee65c2799ZZ53409ac089c542687f0634775402
//&sign=C24D5C335782FADC04DD4863B6A52A5E
//&sign_method=md5&timestamp=1410443760765&v=2.0
