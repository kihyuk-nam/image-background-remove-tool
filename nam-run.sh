wget -q -O ./static/images/in.jpg "$1" > /dev/null

python3 main.py -i ./static/images/in.jpg -o ./static/images/out.png -m $2 -prep None -postp $3

#python3 main.py -i ../images/506121988_thumb_800.jpg -o ../images/after-bag-u2netp-bnb2.png -m u2netp -prep None -postp rtb-bnb2
