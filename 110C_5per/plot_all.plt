set term pngcairo font "Arial,14"

#set mono
set colorsequence classic

data = "modified.dat"
set output "modified.png"

set key left
set size square
set xlabel "Freq."
set ylabel "G', G''"
set y2label "tan d"

set y2tics
set y2range[1e-2:1e1]
set logscale xyy2

set xrange [1e-6:1e10]
set yrange [1e5:]
set y2range[1e-2:1e1]

set format x "10^{%L}"

plot	data u 1:2 axis x1y1 lt 1 ti "G'", \
data u 1:3 axis x1y1 lt 2 ti "G''", \
data u 1:4 axis x1y2 lt 3 ti "tan d"
reset