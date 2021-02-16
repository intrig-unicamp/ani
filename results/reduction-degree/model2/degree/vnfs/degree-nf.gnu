set terminal postscript color eps enhanced
set encoding iso_8859_1
set decimalsign locale; set decimalsign "."

set key top right font ",25" box 3
set xzeroaxis

set boxwidth 0.15 absolute
set border linewidth 2

###########################################################
set xlabel "Nro. NFs" font ",25"
set ylabel "Average Degree" font ",25" offset 1
###########################################################

set tics font ",15"
set xtics('Base' 0, '2' 1,'3' 2, '4' 3, '5' 4, '6' 5)
set xrange [ -0.5 : 5.5 ]
set yrange [0:55]

set output "mod2-degree-nf-100.eps"
plot 'mod2-data.txt' i 0 using (0.):2 with boxes t "Base Line" fs solid 1.0 border lt -1 lc rgb 'black', \
'' i 1 using ($1-0.08):15 with boxes t "Edge-Oriented" fs solid 1.0 border lt -1 lc rgb '#F0F9E8', \
'' i 1 using ($1-0.08):(0):21:22 w yerr notitle lt -1, \
'' i 2 using ($1+0.08):15 with boxes t "Node-Edge-Oriented" fs solid 1.0 border lt -1 lc rgb 'blue', \
'' i 2 using ($1+0.08):(0):21:22 w yerr notitle lt -1
