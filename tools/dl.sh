for i in {1..80}
do
	curl "https://lotv.spawningtool.com/zip/?pro_only=on&patch=150&query=&order_by=play&coop=n&after_played_on=8%2F14%2F20&before_played_on=3%2F14%2F21&before_time=15&after_time=&p=$i" -o "replay_$i.zip"
done
