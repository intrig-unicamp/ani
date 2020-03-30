set terminal postscript color eps enhanced font "Helvetica,26"
set encoding iso_8859_1

set border linewidth 2
set pointsize 3
set key center top
#set xrange [1:8.5]
set xlabel "Percentage of Saved Time" font ",24"
set ylabel "Node Reduction Rate" font ",24" offset 1 textcolor rgb "red"
set y2label "Edge Reduction Rate" font ",24" offset -3 textcolor rgb "blue"
set tics font ",22"

#set logscale x
##set xrange [0:10e1]
#set xrange [1000:55000]
#set mxtics 10
##set logscale x
# 10

#xmax = 10000
#set xrange [0:log10(xmax)]
#unset xtics
#set xtics 1 add ("0" 0, "1" 1)
#set for [i=2:log10(xmax)] xtics add (sprintf("%g",10**(i-1)) i) # Add major tics
#set for [i=1:log10(xmax)] for [j=2:9] xtics add ("" log10(10**i*j) 1) # Add minor tics
#set for [j=1:9] xtics add ("" j/10. 1) # Add minor tics between 0 and 1

set xrange [ 0 : 1 ]
set yrange [ 0 : 1 ]
set yrange [ 0 : 1 ]
#set ytics('0' 0,'0.1' 0.1,'0.2' 0.2,'0.3' 0.3,'0.4' 0.4,'0.5' 0.5,'0.6' 0.6,'0.7' 0.7,'0.8' 0.8,'0.9' 0.9,'1' 1)
#set xtics('0' 0,'0.1' 0.1,'0.2' 0.2,'0.3' 0.3,'0.4' 0.4,'0.5' 0.5,'0.6' 0.6,'0.7' 0.7,'0.8' 0.8,'0.9' 0.9,'1' 1)
set xtics('0' 0,'0.25' 0.25,'0.50' 0.50,'0.75' 0.75,'1' 1)
set ytics('0' 0,'0.25' 0.25,'0.50' 0.50,'0.75' 0.75,'1' 1)
set y2tics('0' 0,'0.25' 0.25,'0.50' 0.50,'0.75' 0.75,'1' 1)
set grid xtics ytics 

set ytics nomirror textcolor rgb "red"
set y2tics nomirror textcolor rgb "blue"

set output "cdf-time-add.eps"

set arrow from -0.205,0.83 to -0.205,0.95 lt 1  lw 3 lc rgb "red" nohead
set arrow from 1.1805,0.83 to 1.1805,0.95 lt 0  lw 3 lc rgb "blue" nohead

plot "cdf-time-add.txt" i 0 using 6:3 notitle with line lt 1  lw 3 lc rgb "red" axis x1y1, \
      "" i 0 using 6:5 notitle with line lt 0  lw 4 lc rgb "blue" axis x1y2



#plot "cdf-time-add.txt" i 0 using 5:1 title "JBIT" with line lt 1  lw 3 lc rgb "red", \
#      "" i 0 using 12:8 title "JBIT\\_AaaS" with line  rgb "blue
