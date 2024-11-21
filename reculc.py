#!/bin/bash
#echo "バックアップ期限までの秒数を入力"
read backuplimit
dirname=[dirname]
hosei=0
echo "指定ディレクトリ:"$dirname
#totalsize=$(du -c $dirname | grep total$ | cut -f 1 | awk '{ printf $1/1024 }')
totalsize=$(du -s testdir_f | cut -f 1)
echo "合計ファイルサイズ:"$totalsize"KB"

# 繰り返し間隔（秒）
interval=[interval]

limitspeed=$((totalsize/backuplimit+hosei))

# rsyncコマンドの実行前に開始時間を記録
start_time=$(date +%s)

#rsync -avhP --append bwlimit==$bwlimit [dirname] [user]@[address]:~/ > outputtest &

# 無限ループで処理を続ける
while true; do
    # 現在の時刻を取得
    restart_time=$(date +%s)
    limitspeed=$((limitspeed+hosei))
    #limitspeed=$(echo "($limitspeed + $hosei) / 1" | bc)

    limitspeed=${limitspeed%.*}

    # rsyncコマンドの実行
    #"${rsync_command[@]}" &
    rsync -rltvhP --append --bwlimit=$limitspeed [dirname] [user]@[address]:~/ > outputtest &
    # rsyncコマンドのプロセスIDを取得
    #rsync_pid=$!
    rsync_pid=$(ps -o pgid= -p $!)
    #kill -CONT $rsync_pid
    # 指定した間隔待つ
    sleep $interval

    # rsyncコマンドを中断
    #kill -TERM $rsync_pid
    kill -TERM $rsync_pid
    echo "ファイル転送を中断しました"

    # 次の繰り返しのために待機時間を考慮して残りの時間を計算
    end_time=$(date +%s)
    elapsed_time=$((end_time - start_time))
    echo "経過時間"$elapsed_time
    transfer_size=$(python3 filesize.py)
    limit=$(($backuplimit-$elapsed_time))
    echo "バックアップ期限まであと"$limit"秒"
    #leftsize=$(echo "scale=2; $totalsize + 7728005  - $transfer_size" | bc)
    leftsize=$(echo "scale=2; $totalsize - $transfer_size" | bc)
    echo "残りファイルサイズ:"$leftsize"KB"

    limitspeed=$(echo "scale=0; $leftsize / $limit" | bc)
    echo "制限速度:"$limitspeed"KB"

    if ((leftsize <= 0)); then
        echo "バックアップが完了しました"
        backup_completed=1
        break
    fi
done
