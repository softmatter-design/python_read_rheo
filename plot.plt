set term pngcairo font "Arial,14"

set colorsequence classic

data = "data.dat"

set output "plot.png"

set size square
set y2tics
set logscale xyy2
set xrange [1:100]
set yrange [1e4:2e9]
set y2range [1e-2:1e1]

set xlabel "Freq."
set ylabel "tan{/Symbol d}"

plot data ind 0 u 1:4 axis x1y2 w l lw 2 lt 1 ti "Tan", \
data ind 0 u 1:2 axis x1y1 w l lw 2 lt 2 ti "G'", \
data ind 0 u 1:3 axis x1y1 w l lw 2 lt 3 ti "G''", \
data ind 1 u 1:4 axis x1y2 w l lw 2 lt 1 noti, \
data ind 1 u 1:2 axis x1y1 w l lw 2 lt 2 noti, \
data ind 1 u 1:3 axis x1y1 w l lw 2 lt 3 noti, \
data ind 2 u 1:4 axis x1y2 w l lw 2 lt 1 noti, \
data ind 2 u 1:2 axis x1y1 w l lw 2 lt 2 noti, \
data ind 2 u 1:3 axis x1y1 w l lw 2 lt 3 noti, \
data ind 3 u 1:4 axis x1y2 w l lw 2 lt 1 noti, \
data ind 3 u 1:2 axis x1y1 w l lw 2 lt 2 noti, \
data ind 3 u 1:3 axis x1y1 w l lw 2 lt 3 noti, \

reset