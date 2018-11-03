module top_level(clk, dig, bus);
	input clk;
	output [7:0] dig;
	output [3:0] bus;
	
	wire f1, f500;
	wire[3:0] t0;
	wire[3:0] t1;
	wire[3:0] t2;
	wire[3:0] t3;
	wire[3:0] d1;
	wire[3:0] b1;
	
	fen_ping IC1(
	clk_50m(clk),
	.clk_1hz(f1),
	.clk_500hz(f500)
	);
	
	ji_shu IC2(
	.clk_1hz(f1), 
	.time0(t0), 
	.time1(t1), 
	.time2(t2), 
	.time3(t3)
	);
	
	decode IC3(
	.in_4(d1), 
	.bus_4(bus),
	.out_8(dig)
	);
	
	scanning IC4(
	.clk_500hz(f500), 
	.time0(t0), 
	.time1(t1), 
	.time2(t2), 
	.time3(t3), 
	.dig_4(d1), 
	.bus_4(bus)
	);

endmodule