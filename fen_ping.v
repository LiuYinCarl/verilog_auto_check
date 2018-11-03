module fen_ping(clk_50m, clk_1hz, clk_500hz);

	input clk_50m;
	output reg clk_1hz;
	output reg clk_500hz;
	
	reg[27:0] count;
	reg[19:0] count2;
	
	always@(posedge clk_50m)
	begin
		if(count < 50000000)
		begin
			count = count + 1;
			if(count < 25000000)
				clk_1hz = 0;
			else clk_1hz = 1;
		end
		else count = 0;
	end
	
	always@(posedge clk_50m)
	begin
		if(count2 < 100000)
		begin
			count2 = count2 + 1;
			if(count2 < 50000)
				clk_500hz = 0;
			else clk_500hz = 1;
		end
		else count2 = 0;
	end
	
endmodule