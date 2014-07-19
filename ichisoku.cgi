#!/usr/bin/perl

##################################
#一問即答ver.1.00               ##
##################################
##  (c)Rupy                     ##
##  FIRST RELEASE:2008/5/06     ##
##  LAST UPDATE:2008/5/06       ##
##  http://rupy.jp/             ##
##                              ##
##################################

use CGI;

#=====================
#基本項目（自分の環境に応じて書き換えてください）
#=====================

#ichisoku.cgiからみた問題ファイルの存在するディレクトリへの相対パス
$FILE_FIELD = "mondai/";
#ファイルの選択の決定ボタン名
$SUBMIT = "OK！";

#=====================
#メインプログラム
#=====================
$CHARSET = "Shift_JIS";#文字コードの指定

print"Content-type: text/html; charset=\"$CHARSET\"\n\n";
$cgi = CGI::new();
$PAGE = 0;
$MODE = $cgi->param('mode');#モード
$FILE = $cgi->param('file');#ファイル名
$PAGE = $cgi->param('page');#現在のページ
$OPT = $cgi->param('opt');#オプション
$OK = $cgi->param('ok');#
$KOTAE = $cgi->param('kotae');#

@DATA = ();
@OKEYs = ();
if($MODE eq 'test'){
	&dataRead();
}

$TOPIC = shift @DATA;#１行目はタイトル
$LAST = $#DATA;#ファイルの最後の行数（添え字）
$END = int($#DATA / 2);#添え字÷２
$OPTION = "";
@SUBJECT = "";

if($MODE eq 'opt'){
	&selectOption();
	exit;
}elsif($FILE eq ""){
	&selectFile();
	exit;
}

if($MODE eq 'test'){
	if($OPT eq 'opp'){
		&gyakuMode();
		$OPTION = "逆出題";
	}
	if($OPT eq 'ord'){
		&gyakuMode();
		$OPTION = "逆ランダム";
	}

	elsif($OPT eq 'list'){
		&printList();
		exit;
	}
	if(($OPT eq 'rnd')or($OPT eq 'ord')){
		@SUBJECT = &setRandom();
		$OPTION = "ランダム出題";
	}
	else{
		@SUBJECT = &setQuestion();	
	}
	&printIchimonSokuto(@SUBJECT);
	exit;
}
exit;
#=====================
#ファイルセレクト
#=====================
sub selectFile{
print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<meta http-equiv="Content-Type" content="text/html; charset=$CHARSET">
<http><head><title>ファイルセレクト</title></head>
<body bgcolor="#99FF77">
END
#ディレクトリの中身を取得し、配列@listにいれる
	@list = ();
	opendir(DIR, "$FILE_FIELD")
		or &printErrorPage("$FILE_FIELDのディレクトリオープン失敗");
	while($DIREC = readdir(DIR)){
		if($DIREC !~ /^\.$/){
			push(@list, $DIREC);
		}
	}
	closedir(DIR);


	print"<h1>問題ファイル選択</h1>";
	print"<form action=\"$ENV{'SCRIPT_NAME'}\" method=\"GET\">";
	#ディレクトリの中身でテキストファイルを判別する
	foreach $file (@list){
		if($file =~ /^.+\.txt$/){
			print"<input type=\"radio\" name=\"file\" value=\"$file\">";
			print"$DIR$file<br>\n";
		}
	}
	print <<END;
<input type="hidden" name="mode" value="opt">
<input type="submit" value="$SUBMIT">
</form>
</body>
</html>
END
exit;
}
#=====================
#記事読み込み
#=====================
sub dataRead{
	open(FILE, "<$FILE_FIELD$FILE")
		or &printErrorPage("$FILE_FIELD$FILEのファイルが開けません");
	flock(FILE,2);
	while($tmpl = <FILE>){
#		chop ($tmpl);
		if($tmpl =~ /^\s*$/){next;}
		push(@DATA,$tmpl);
	}
	flock(FILE,8);
	close(FILE);

	my $tmp = "";
	if($OK =~ /^,\d+$/){
		$OK =~ s/,//;#初めのコンマを取る
	}
	foreach $tmp (split(/,/, $OK)){
	push (@OKEYs,$tmp);#スカラーを配列に分ける
	}
}
#=====================
#モードセレクト
#=====================
sub selectOption{
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<meta http-equiv="Content-Type" content="text/html; charset=$CHARSET">
<http>
<head><title>モードセレクト</title></head>
<body>
<h1>モードセレクト</h1>
END
	if(open(FILE,"<$FILE_FIELD$FILE")){
		$title = <FILE>;
		chop $title;
	close (FILE);
	}
	print <<END;
<h2>$title</h2>
ファイル名：$FILE<br>
<form action="$ENV{'SCRIPT_NAME'}" method="GET">
<p>モード選択<br>
<select name="opt">
<option value="no">普通出題</option>
<option value="opp">逆出題</option>
<option value="rnd">ランダム出題</option>
<option value="ord">逆ランダム</option>
<option value="list">問題一覧表\示</option>
</select>
</p>
END

print<<END;
<input type="hidden" name="file" value="$FILE">
<input type="hidden" name="mode" value="test">
<input type="submit" value="$SUBMIT">
</form>
</body>
</html>
END
exit;
}
#=====================
#逆出題用
#=====================
sub gyakuMode{
	my @tmp1 = ();
	my @tmp2 = ();
	until(0 >= $#DATA){
		push(@tmp1,shift @DATA);
		push(@tmp2,shift @DATA);
	}
	until($LAST == $#DATA){
		push(@DATA,shift(@tmp2));
		push(@DATA,shift(@tmp1));
	}
}
#=====================
#問題ページ（デザインはここを書き換えればよい）
#=====================
sub printIchimonSokuto{
	my ($title, $answer, $nigate, $number, $question, $move, $allQuestion, $back) = @_;
	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<meta http-equiv="Content-Type" content="text/html; charset=$CHARSET">
<html>
<head><title>$title</title></head>
<body style="background-color:pink;">
<p>
答え：$answer
<hr>
あなたの答え:$KOTAE
</p>
<h1 style="background-color:yellow;">$number</h1>
$nigate
<p style="background-color:#88ffff;margin:0 10;padding:10;">
$question<br>
</p>
$move
$allQuestion<br>
<a href="$ENV{'SCRIPT_NAME'}?mode=opt&file=$FILE">モード切り替え</a>
<a href="$ENV{'SCRIPT_NAME'}">ファイルの選択</a>
</body>
</html>
END
}
#=====================
#一問即答（普通出題）
#=====================
sub setQuestion
{
	my $ans = 0;
	my $ques = 0;
	my $prevPage = 0;
	my $nextPage = 0;
	my $addTen = 0;
	my $subtractTen = 0;
	#ページ数が０のとき答えを最後からもってくる
	#また前のページは最後のページ
	if($PAGE == 0){
		$ans = $LAST;
		$ques = 0;
		$prevPage = $END;
	}
	#０ページ以外はページに２を掛けた行が前の答えとなる
	#(０ページから始まるから)
	#質問は答えの次なので１を足す
	else{
		$ans = $PAGE * 2 - 1;#($ansは添え字だから-1)
		$ques = $ans + 1;
		$prevPage = $PAGE-1;
	}
	#最後のページでない時
	#次のページは今のページ数に１を足したもの
	if($PAGE < $END){
		$nextPage = $PAGE+1;
	}
	#最後のページであれば
	#次のページは始めに戻る
	else{
		$nextPage = 0;
	}

	my $num = $PAGE + 1;#現在何問目か。
	my $all = $END+1;#$ENDは添え字だから+1

	$addTen = $PAGE + 10;
	if($addTen > $END){
		$addTen = $addTen - ($END+1) ;#$ENDは添え字だから+1
	}
	$subtractTen = $PAGE - 10;
	if($subtractTen < 0){
		$subtractTen = ($END+1) + $subtractTen;#$ENDは添え字だから+1
	}	
	my $title = "$TOPIC $num問目$OPTION";
	my $answer = "$DATA[$ans]";
	my $nigate=<<END;
<form action="$ENV{'SCRIPT_NAME'}" method="GET">
<input type="hidden" name="mode" value="$MODE">
<input type="hidden" name="file" value="$FILE">
<input type="hidden" name="opt" value="$OPT">
<input type="hidden" name="page" value="$nextPage">
<input type="text" name="kotae">
<input type="submit" value="答える">
</form>
END
	my $number = "$num問目$OPTION　〜$TOPIC";
	my $question="$DATA[$ques]";
	my $move=<<END;
<a href="$ENV{'SCRIPT_NAME'}?file=$FILE&mode=$MODE&opt=$OPT&page=$prevPage">前へ</a>
<a href="$ENV{'SCRIPT_NAME'}?file=$FILE&mode=$MODE&opt=$OPT&page=$nextPage">次へ</a><br>
<a href="$ENV{'SCRIPT_NAME'}?file=$FILE&mode=$MODE&opt=$OPT&page=0">はじめ</a>
<a href="$ENV{'SCRIPT_NAME'}?file=$FILE&mode=$MODE&opt=$OPT&page=$subtractTen">-10</a>
<a href="$ENV{'SCRIPT_NAME'}?file=$FILE&mode=$MODE&opt=$OPT&page=$addTen">+10</a>
<a href="$ENV{'SCRIPT_NAME'}?file=$FILE&mode=$MODE&opt=$OPT&page=$END">最後</a><br>
<form action="$ENV{'SCRIPT_NAME'}" method="GET">
<input type="text" name="page">
<input type="hidden" name="mode" value="$MODE">
<input type="hidden" name="file" value="$FILE">
<input type="hidden" name="opt" value="$OPT">
<input type="submit" value="移動">
</form>
END

my $allQuestion = "全部で$all問あります。";
	return ($title, $answer, $nigate, $number, $question, $move, $allQuestion);
}
#=====================
#一問即答（ランダム）
#=====================
sub setRandom{
	my $ans = 0;
	my $ques = 0;
	my $prevPage = 0;
	my $nextPage = 0;

	my $rnd = 0;

	#問題数は
	$all = $END+1;#$ENDは添え字だから+1
	$ii=0;
	$ans = $PAGE * 2 +1;

	$nokori = $END - $#OKEYs;
	print"残りの問題数は$nokori問です。";

#ここから重複出題を避けるシステム
	RND:$rnd = int(rand($all));
	if($END > $#OKEYs){#全問題数と問題解答数を比較(添え字同士)
		foreach $key(@OKEYs){
			$ii++;
			if($rnd == $key){goto RND}
			if($ii >100000){print"オーバー";last;}
		}
	}else{
	print"一通り終了しました。";
	$OK = "";
	}
#ここまで重複出題を避けるシステム
	$PAGE = $rnd;
	$ques = $PAGE * 2;
#ページ数に１を足したもの。現在何問目か。
	my $num = $PAGE + 1;
my $title = "$TOPIC $num問目$OPTION";
my $answer = "$DATA[$ans]";
my $nigate="";

my $number = "$num問目$OPTION　〜$TOPIC";
my $question = "$DATA[$ques]";

#重複拒否の場合
my $okey = "";
		$okey="&ok=$OK,$PAGE";

my $move=<<END;
<a href="$ENV{'SCRIPT_NAME'}?file=$FILE&mode=test&opt=$OPT&page=$PAGE$okey">次へ</a><br>
END

my $allQuestion="全部で$all問あります。";

	return ($title, $answer, $nigate, $number, $question, $move, $allQuestion);
}
#=====================
#問題一覧表示
#=====================
sub printList{
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<meta http-equiv="Content-Type" content="text/html; charset=$CHARSET">
<http>
<head><title>問題一覧表\示</title></head>
<body style="background-color:pink;">
END
print <<END;
<h1>$TOPIC</h1>
<h2>問題一覧表\示</h2>
END
	my $i = 0;
	foreach $listup(@DATA){
		if($i % 2 == 1){
			print"<div style=\"background-color:#88ffff\;padding:0 10;\">";
		}
		else{
			print"<div style=\"background-color:yellow;padding:0 10;\">";
		}
		print"$listup</div>\n";
		$i++;
	}
	print <<END;
<a href="$ENV{'SCRIPT_NAME'}">ファイルの選択</a>
</body>
</html>
END
exit;
}
#=====================
#エラー発生
#=====================
sub printErrorPage{
print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<meta http-equiv="Content-Type" content="text/html; charset=$CHARSET">
<http>
<head><title>エラーページ</title></head>
<body>
<h1>エラーが発生しました</h1>
<p>$_[0]</p>
<p><a href=\"$ENV{'SCRIPT_NAME'}\">戻る</a></p>
</body>
</html>
END
exit;
}