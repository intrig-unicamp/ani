set terminal postscript color eps enhanced
set encoding iso_8859_1
set decimalsign locale; set decimalsign "."

set key top left font ",25" box 3
set xzeroaxis

set boxwidth 0.15 absolute
set border linewidth 2

###########################################################
set xlabel "Network Inventory Size" font ",25"
set ylabel "Average Degree" font ",25" offset 1
###########################################################

set tics font ",15"
set xtics('50' 1,'100' 2, '150' 3, '200' 4, '250' 5)
set xrange [ 0.5 : 5.5 ]
set yrange [0:52]

set output "mod1-degree.eps"
plot 'mod1-data.txt' i 0 using ($1-0.225):2 with boxes t "Base Line" fs solid 1.0 border lt -1 lc rgb 'black', \
'' i 0 using ($1-0.075):15 with boxes t "Node-Oriented" fs solid 1.0 border lt -1 lc rgb '#2B8CBE', \
'' i 0 using ($1-0.075):(0):21:22 w yerr notitle lt -1, \
'' i 1 using ($1+0.075):15 with boxes t "Edge-Oriented" fs solid 1.0 border lt -1 lc rgb '#F0F9E8', \
'' i 1 using ($1+0.075):(0):21:22 w yerr notitle lt -1, \
'' i 2 using ($1+0.225):15 with boxes t "Node-Edge-Oriented" fs solid 1.0 border lt -1 lc rgb 'blue', \
'' i 2 using ($1+0.225):(0):21:22 w yerr notitle lt -1
