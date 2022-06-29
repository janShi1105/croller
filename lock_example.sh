#!bin/zsh
function main_command(){
	echo 'コマンドを実行しています...';
	sleep 30;
}

PIDFILE=/tmp/lock_example.pid

if [ -f $PIDFILE ];then
	PID=$(cat $PIDFILE);

	ps -p $PID > /dev/null 2>&1;

	if [ $? -eq 0 ];then
		echo "既に起動しています. PID: $PID";
		exit 1;
	else
		echo "$PIDFILE は存在しますがプロセスは起動していません";
		echo "状況を確認して問題がなければ $PIDFILE を削除して再実行してください";
		exit 1;
	fi
fi

echo $$ > $PIDFILE;
echo "プロセスを起動します. プロセスID: $(cat $PIDFILE)"
main_command;
rm $PIDFILE;
