module scanning(clk_500hz, time0, time1, time2, time3, dig_4, bus_4);

	input clk_500hz;
	input[3:0] time0;
	input[3:0] time1;
	input[3:0] time2;
	input[3:0] time3;
	
	output reg[3:0] dig_4;
	output reg[3:0] bus_4;
	
	reg[11:0] count;
	
	always@(posedge clk_500hz)
	begin
		if(count == 3)
			count = 0;
		else count = count + 1;
	end
	
	always@(count)
	begin
		if(count == 0)
		begin
			dig_4 = time0;
			bus_4 = 4'b0111;
		end
		else if(count == 1)
		begin
			dig_4 = time1;
			bus_4 = 4'b1011;
		end
		else if(count == 2)
		begin
			dig_4 = time2;
			bus_4 = 4'b1101;
		end
		else 
		begin
			dig_4 = time3;
			bus_4 = 4'b1110;
		end
	end
endmodule