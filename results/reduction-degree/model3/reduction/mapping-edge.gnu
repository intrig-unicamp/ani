set terminal postscript color eps enhanced font "Helvetica,26"
set encoding iso_8859_1

set key tmargin horizontal
set xzeroaxis

set xlabel "Network Inventory Size" font ",24"
set ylabel "Normalized Reduction (%)" font ",24" offset 1
set tics font ",22"

set boxwidth 0.2 absolute
set xrange [ 0.5 : 5.5 ]
set yrange [ -5 : 105] noreverse nowriteback
set xtics('50' 1,'100' 2, '150' 3, '200' 4, '250' 5)

set output "./edge/mod3-mapping-edge.eps"
plot './mod3-data.txt' i 0 using ($1-0.24):8:7:11:10 with candlesticks fs pattern 2 t "Node-Oriented" lt 1 lw 3 lc rgb "green" whiskerbars, \
'' i 0 using ($1-0.24):9:9:9:9 with candlesticks lt -1 lw 4 lc rgb "black" notitle, \
'' i 0 using ($1-0.24):($9+2):9 with labels notitle font "Helvetica-Bold,10", \
'' i 1 using ($1+0.):8:7:11:10 with candlesticks fs solid 0.25 t "Edge-Oriented" lt 1 lw 3 lc rgb "red" whiskerbars, \
'' i 1 using ($1+0.):9:9:9:9 with candlesticks lt -1 lw 4 lc rgb "black" notitle ,\
'' i 2 using ($1+0.24):8:7:11:10 with candlesticks fs pattern 5 t "Node/Edge-Oriented" lt 1 lw 3 lc rgb "blue" whiskerbars, \
'' i 2 using ($1+0.24):9:9:9:9 with candlesticks lt -1 lw 4 lc rgb "black" notitle ,\
