set term pngcairo font "Arial,14" 
set colorsequence classic 
# 
data = "data.dat" 
set output "plot.png"
#
set size square
set y2tics
set logscale xyy2

#
#set xrange [1e-2:1e5]
set yrange [1e4:2e9]
set y2range [1e-2:1e1]

#
set xlabel "Freq."
set ylabel "G"
set y2label "tan{/Symbol d}"

plot data ind 0 u 1:4 axis x1y2 w l lc 0 noti, \
data ind 1 u 1:4 axis x1y2 w l lc 1 noti, \
data ind 2 u 1:4 axis x1y2 w l lc 2 noti, \
data ind 3 u 1:4 axis x1y2 w l lc 3 noti, \
data ind 4 u 1:4 axis x1y2 w l lc 4 noti, \
data ind 5 u 1:4 axis x1y2 w l lc 5 noti, \
data ind 6 u 1:4 axis x1y2 w l lc 6 noti, \
data ind 7 u 1:4 axis x1y2 w l lc 7 noti, \
data ind 8 u 1:4 axis x1y2 w l lc 8 noti, \
data ind 9 u 1:4 axis x1y2 w l lc 9 noti, \
data ind 10 u 1:4 axis x1y2 w l lc 10 noti, \
data ind 11 u 1:4 axis x1y2 w l lc 11 noti, \
data ind 12 u 1:4 axis x1y2 w l lc 12 noti, \
data ind 13 u 1:4 axis x1y2 w l lc 13 noti, \
data ind 14 u 1:4 axis x1y2 w l lc 14 noti, \
data ind 15 u 1:4 axis x1y2 w l lc 15 noti, \
data ind 16 u 1:4 axis x1y2 w l lc 16 noti, \
data ind 17 u 1:4 axis x1y2 w l lc 17 noti, \
data ind 18 u 1:4 axis x1y2 w l lc 18 noti, \
data ind 19 u 1:4 axis x1y2 w l lc 19 noti, \
data ind 20 u 1:4 axis x1y2 w l lc 20 noti, \
data ind 21 u 1:4 axis x1y2 w l lc 21 noti, \
data ind 22 u 1:4 axis x1y2 w l lc 22 noti, \
data ind 23 u 1:4 axis x1y2 w l lc 23 noti, \
data ind 24 u 1:4 axis x1y2 w l lc 24 noti, \


reset