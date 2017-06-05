<?php
ini_set('display_errors',1);            //错误信息
ini_set('display_startup_errors',1);    //php启动错误信息
error_reporting(-1);                    //打印出所有的 错误信息
ini_set('error_log', dirname(__FILE__) . '/error_log'); //将出错信息输出到一个文本文件

//需要修改的2个值
$phone = "";
$cookie = "";
$id = ""; //http://sc.ftqq.com/ 通知微信的
//默认一页显示20个活动
$eventsnum = 20; 
$eventids = array();

$ch=curl_init(); 
curl_setopt($ch,CURLOPT_COOKIE,$cookie); 
curl_setopt($ch,CURLOPT_USERAGENT,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36");
curl_setopt($ch,CURLOPT_HEADER,0); 
curl_setopt($ch,CURLOPT_RETURNTRANSFER,1); 


//首页
function get_events($ch){
	curl_setopt($ch,CURLOPT_HTTPGET,1); 
	curl_setopt($ch,CURLOPT_URL,'http://s.dianping.com/event/shanghai'); 
	$data = curl_exec($ch);
	return $data;
}

// 得到总共的活动数量
function get_total_events($data){
	//正则匹配 title="全部">全部(252)</a></span>
	preg_match('/全部\((.*)\)/',$data,$count);
	return $count[1];
}

function get_more_events($ch,$page){
	curl_setopt($ch,CURLOPT_POST,1); 
	curl_setopt($ch,CURLOPT_URL,'http://s.dianping.com/ajax/json/activity/offline/moreActivityList'); 
	curl_setopt($ch, CURLOPT_POSTFIELDS, "page=".$page);
	$data = curl_exec($ch);
	return $data;
}

//首页匹配HTML
function get_event_ids($data){
	//, title:'优悦派游艇别墅轰趴馆——价值9980元轰趴体验免费抢', eventid:457000446}
	//preg_match_all('/title:\'\(.*)\'/',$data,$titles);
	preg_match_all('/eventid:(.*)\}/',$data,$eventids);
	return $eventids;
}

//其他页是json
function get_more_event_ids($data){
	//"\/event\/631067128\"
	preg_match_all("/event\\\\\/(\d+)\\\\\"/",$data,$eventids);

	$result = array();

	for ($i=0; $i<count($eventids[0]); $i++) {
		$str = $eventids[0][$i];
		preg_match("/(\d+)/",$str,$tmp);
		$result[] = $tmp[0];
	} 

	return $result;
}

function signup_event($ch,$eventid,$phone){
	curl_setopt($ch,CURLOPT_POST,1); 
	curl_setopt($ch,CURLOPT_URL,'http://s.dianping.com/ajax/json/activity/offline/saveApplyInfo'); 
	curl_setopt($ch,CURLOPT_POSTFIELDS,"offlineActivityId=".$eventid."&phoneNo=".$phone."&marryStatus=0"); 
	$data = curl_exec($ch);
	return $data;
}


$indexdata = get_events($ch);

//活动总数
$eventcount = get_total_events($indexdata);

//总页数
$pagecount =  $eventcount / $eventsnum +1;


$eventids = array_merge($eventids, get_event_ids($indexdata)[1]);

for ($i = 2; $i < $pagecount; $i++) {
	$result = get_more_events($ch,$i);
	$result = get_more_event_ids($result);

	$eventids = array_merge($eventids, $result);
}

$eventids = array_unique($eventids);

$len = count($eventids);
for($i = 0; $i < $len;$i++){
	$result = signup_event($ch,$eventids[$i],$phone);
	//file_put_contents("log.txt", $result, FILE_APPEND);

    /*
    if(strpos($result, "参数无效")){
        file_get_contents("http://sc.ftqq.com/".$id".send?text=".urlencode("点评需要更新Cookies了！"));
        break;
    }*/
}



curl_close($ch);

?>