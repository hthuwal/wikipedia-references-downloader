download_dir=$1

function get_ext()
{
	local link=$1
	local filename=$(basename -- "$link")
	local extension="${filename##*.}"

	echo $filename
	if [[ extension == "" ]]
	then
		extension=".html"
	fi
	echo $extension
}

function download()
{
	local cur=$(pwd)
	local dir=$(dirname "$1")
	local refer_file=$(basename "$1")

	cd "$dir"
	rm -f log.txt uri.txt
	count=0

	while read link
	do 
		count=$((count+1))
		echo "$count" "$link" >> log.txt
		echo -e "$link" "\n\tout=$count" >> uri.txt
	done < "$refer_file"
	
	aria2c -c -x 16 -s 16 -q --connect-timeout=5 -i uri.txt
	exit_code=$?

	rm uri.txt
	cd - 
	return $exit_code
}


function auto_extension()
{
	echo "Applying Correct Extensions..."
	local dir=$(dirname "$1")
	cd "$dir"
	for each in *
	do
		local mime_type=$(file --mime-type $each | awk '{print $2}')
		local ext=$(grep -v '^\#' /etc/mime.types | grep -w "$mime_type" | head -n 1 | awk '{ print$2}')
		if [[ ! -z $ext ]]
		then
	    	mv "$each" "${each%%.*}.${ext,,}"
	    fi
	done
	cd -
}

num_file=0
find "$download_dir" -iname "*references.txt" | sort > "list_of_ref.txt"
while read file
do
	num_file=$((num_file+1))
	echo $num_file":" $file
	download "$file"
	auto_extension "$file"
	test $? -eq 7 && break
done < "list_of_ref.txt"

rm "list_of_ref.txt"


